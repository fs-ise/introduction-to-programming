#!/usr/bin/env node

/** Generate the static QR-code images used by the course materials. */

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const zlib = require("zlib");

const ROOT = path.resolve(__dirname, "..");
const QR_RENDERER = path.join(ROOT, "_extensions/jmbuhr/qrcode/qrcode.js");
const QR_CODES = [
  {
    destination:
      "https://fs-ise.github.io/introduction-to-programming/student_guide/language-settings.html",
    output: path.join(ROOT, "images/qr_excel_language_settings.png"),
  },
];
const IMAGE_SIZE = 600;

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ (crc & 1 ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function pngChunk(type, data) {
  const typeBuffer = Buffer.from(type, "ascii");
  const chunk = Buffer.concat([typeBuffer, data]);
  const length = Buffer.alloc(4);
  const checksum = Buffer.alloc(4);
  length.writeUInt32BE(data.length);
  checksum.writeUInt32BE(crc32(chunk));
  return Buffer.concat([length, chunk, checksum]);
}

function encodeGrayscalePng(pixels, width, height) {
  const header = Buffer.alloc(13);
  header.writeUInt32BE(width, 0);
  header.writeUInt32BE(height, 4);
  header[8] = 8; // bit depth
  header[9] = 0; // grayscale

  const scanlines = Buffer.alloc((width + 1) * height);
  for (let row = 0; row < height; row += 1) {
    const offset = row * (width + 1);
    scanlines[offset] = 0; // no PNG row filter
    pixels.copy(scanlines, offset + 1, row * width, (row + 1) * width);
  }

  return Buffer.concat([
    Buffer.from("89504e470d0a1a0a", "hex"),
    pngChunk("IHDR", header),
    pngChunk("IDAT", zlib.deflateSync(scanlines, { level: 9 })),
    pngChunk("IEND", Buffer.alloc(0)),
  ]);
}

function renderQrCode(destination) {
  const pixels = Buffer.alloc(IMAGE_SIZE * IMAGE_SIZE, 255);
  const context = {
    fillStyle: "#fff",
    fillRect(left, top, width, height) {
      const value = this.fillStyle === "#000" ? 0 : 255;
      for (let row = top; row < top + height; row += 1) {
        pixels.fill(value, row * IMAGE_SIZE + left, row * IMAGE_SIZE + left + width);
      }
    },
  };
  const canvas = {
    setAttribute() {},
    style: {},
    getContext() {
      return context;
    },
  };
  const element = {
    firstChild: null,
    getAttribute(name) {
      return {
        "data-qrcode": destination,
        "data-width": String(IMAGE_SIZE),
        "data-height": String(IMAGE_SIZE),
      }[name];
    },
    appendChild() {},
  };
  const document = {
    readyState: "complete",
    querySelectorAll() {
      return [element];
    },
    createElement() {
      return canvas;
    },
  };

  vm.runInNewContext(fs.readFileSync(QR_RENDERER, "utf8"), { document });
  return encodeGrayscalePng(pixels, IMAGE_SIZE, IMAGE_SIZE);
}

for (const { destination, output } of QR_CODES) {
  fs.writeFileSync(output, renderQrCode(destination));
  process.stdout.write(`Generated ${path.relative(ROOT, output)} for ${destination}\n`);
}

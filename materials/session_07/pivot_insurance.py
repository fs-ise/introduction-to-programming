import pandas as pd

insurance = pd.read_excel("data/insurance.xlsx")

pd.options.display.float_format = "{:.2f}".format

# 1.Calculate the average of InsuredValue per state using the pivot_table() function.
pd.pivot_table(insurance, index="State", values="InsuredValue", aggfunc="mean")

# 2. Calculate the average of InsuredValue per state splitted by location.
pd.pivot_table(
    insurance,
    index="State",
    columns="Location",
    values="InsuredValue",
    aggfunc="mean",
    fill_value=0,
)
# Remark: The parameter fill_value=0 replaces NaN with 0

# 3. Calculate the average of InsuredValue per state splitted by region where a flood or an earthquake is part of the contract.
pd.pivot_table(
    insurance[(insurance.Flood == "Y") | (insurance.Earthquake == "Y")],
    index="State",
    columns="Region",
    values="InsuredValue",
    aggfunc="mean",
    fill_value=0,
)

# 4. Calculate the average of InsuredValue per state splitted by construction where a flood and an earthquake is part of the contract.
pd.pivot_table(
    insurance[(insurance.Flood == "Y") & (insurance.Earthquake == "Y")],
    index="State",
    columns="Construction",
    values="InsuredValue",
    aggfunc="mean",
    fill_value=0,
)

# 5. Calculate the sum of InsuredValue per location and business type splitted by region.
pd.pivot_table(
    insurance,
    index=["Location", "BusinessType"],
    columns="Region",
    values="InsuredValue",
    aggfunc="sum",
    fill_value=0,
)

# 6. Repeat the previous query and add printing the column sums at the end of the table.
pivot_df = pd.pivot_table(
    insurance,
    index=["Location", "BusinessType"],
    columns="Region",
    values="InsuredValue",
    aggfunc="sum",
    fill_value=0,
)
pivot_df.loc["Total"] = pivot_df.sum()
print(pivot_df)

# 7. Create a bar chart displaying the numbers of contracts for the locations splitted by state.
pivot_df = pd.pivot_table(
    insurance,
    index="Location",
    columns="State",
    values="InsuredValue",
    aggfunc="count",
    fill_value=0,
)
pivot_df.plot(kind="bar")

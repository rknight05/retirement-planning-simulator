import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_age = int(input("Current Age: "))
retirement_age = int(input("Retirement Age: "))
years = retirement_age - current_age
initial_savings = int(input("Initial Savings: "))
annual_cont = int(input("Annual Contribution: "))
target = int(input("Target Savings: "))
int_rate = 0.07
inflation_rate = 0.03



simulations = 10000

volatility = 0.15
inflation_volatility = 0.003

final_balances = []
all_balances = np.zeros((simulations, years + 1))
for simulation in range(simulations):
    balance = initial_savings
    all_balances[simulation, 0] = balance
    cumulative_inflation = 1
    for year in range(years):
        annual_return = np.random.normal(int_rate, volatility)
        annual_return = max(annual_return, -0.99)
        balance = balance * (1 + annual_return) + annual_cont
        all_balances[simulation, year + 1] = balance
        annual_inflation = np.random.normal(inflation_rate,inflation_volatility)
        cumulative_inflation *= (1 + annual_inflation)
    real_balance = balance / cumulative_inflation
    final_balances.append(real_balance)
final_balances = np.array(final_balances)

print("Average:", round(np.mean(final_balances)))
print("Median:", round(np.median(final_balances)))
print("10th Percentile:", round(np.percentile(final_balances, 10)))
print("90th Percentile:", round(np.percentile(final_balances, 90)))
target_prob = round(np.mean(final_balances >= target),2)
print("Probability of reaching target:", target_prob * 100, "%")

data = np.array(final_balances)
lower = np.percentile(data, 1)
upper = np.percentile(data, 99)
plt.figure(figsize=(12, 6))
plt.hist(data, bins=50, range=(lower, upper), edgecolor="black")
plt.axvline(np.median(data), color="red", linestyle="dashed", label=f"Median: ${np.median(data):,.0f}")
plt.axvline(np.mean(data), color="blue", linestyle="dashed", label=f"Mean: ${np.mean(data):,.0f}")
plt.title("Distribution of Retirement Balances (Central 98%)")
plt.xlabel("Inflation-Adjusted Retirement Balance ($)")
plt.ylabel("Number of Simulations")

plt.legend()
plt.ticklabel_format(style="plain", axis="x")
plt.tight_layout()
plt.show()


median_balances = np.median(all_balances, axis=0)
thirdquarter_balances = np.percentile(all_balances, 75, axis=0)
firstquarter_balances = np.percentile(all_balances, 25, axis=0)
plt.plot(range(years + 1), median_balances, label = "Median", color = "blue")
plt.plot(range(years + 1), thirdquarter_balances, label = "75th Percentile", linestyle = "dashed", color = "orange")
plt.plot(range(years + 1), firstquarter_balances, label = "25th Percentile", linestyle = "dashed", color = "green")
plt.fill_between(range(years + 1), firstquarter_balances, thirdquarter_balances, alpha = 0.2)
plt.title("Median Retirement Savings Growth")
plt.xlabel("Years")
plt.ylabel("Account Balance (Millions of Dollars)")
plt.legend()
plt.show()



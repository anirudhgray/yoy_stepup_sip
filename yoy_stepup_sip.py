import matplotlib.pyplot as plt
import itertools
import typer
from rich.console import Console
from rich.table import Table
import csv

app = typer.Typer()
console = Console()

def calculate_yearly_growth(
    initial_lump_sum: float,
    monthly_sip: float,
    annual_step_up: float,
    annual_rate_of_return: float,
    years: int,
    inflation_rate: float = 0.0  # <-- NEW PARAM
):
    monthly_rate_of_return = (1 + annual_rate_of_return / 100) ** (1/12) - 1
    portfolio_value = initial_lump_sum
    total_invested = initial_lump_sum

    yearly_data = []

    for year in range(1, years + 1):
        current_sip = monthly_sip * ((1 + annual_step_up / 100) ** (year - 1))
        for _ in range(12):
            portfolio_value += current_sip
            portfolio_value *= (1 + monthly_rate_of_return)
        total_invested += current_sip * 12

        # Inflation adjustment
        inflation_multiplier = (1 + inflation_rate / 100) ** year
        real_value = portfolio_value / inflation_multiplier
        real_gain = real_value - total_invested

        yearly_data.append({
            "year": year,
            "invested": round(total_invested),
            "value": round(portfolio_value),
            "gain": round(portfolio_value - total_invested),
            "real_value": round(real_value),
            "real_gain": round(real_gain),
            "invested_crore": round(total_invested / 1e7, 2),
            "value_crore": round(portfolio_value / 1e7, 2),
            "real_value_crore": round(real_value / 1e7, 2)
        })

    return yearly_data


def plot_growth(years: int, yearly_data: list[dict], title: str, color: str = 'b', marker: str = 'o', label: str = "Step-up: NA", show_invested: bool = False, show_nominal: bool = False):
    # Determine the interval for displaying data points based on the number of years
    if years <= 10:
        interval = 1
    elif years <= 25:
        interval = 2
    else:
        interval = 3

    # Filter yearly data based on the interval
    filtered_yearly_data = [d for d in yearly_data if d["year"] % interval == 0 or d["year"] == years]

    years_list = [d["year"] for d in filtered_yearly_data]
    values = [d["value_crore"] for d in filtered_yearly_data]
    invested_amounts = [d["invested_crore"] for d in filtered_yearly_data]
    real_values = [d["real_value_crore"] for d in filtered_yearly_data]

    plt.plot(years_list, real_values, marker=marker, linestyle=':', color=color, label=f"Real Value {label}")
    for x, y in zip(years_list, real_values):
        plt.text(x, y, f'{y:.2f}', fontsize=8, ha='right')
    if show_nominal:
        plt.plot(years_list, values, marker=marker, linestyle='-', color=color, label=f"Nominal Value {label}")
        for x, y in zip(years_list, values):
            plt.text(x, y, f'{y:.2f}', fontsize=8, ha='right')
    if show_invested:
        plt.plot(years_list, invested_amounts, marker=marker, linestyle='--', color=color, label=f"Invested Amount {label}")
        for x, y in zip(years_list, invested_amounts):
            plt.text(x, y, f'{y:.2f}', fontsize=8, ha='right')
    
    plt.title(title)
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value (INR Crore)')
    plt.grid(True)
    plt.legend()


@app.command()
def plot_multiple_growths(
    initial_lump_sum: float = typer.Option(700000, help="Initial lump sum investment in INR"),
    sip_amounts: str = typer.Option("70000,120000,250000", help="Comma-separated list of SIP amounts in INR"),
    step_ups: str = typer.Option("0,10", help="Comma-separated list of annual step-up percentages"),
    rates_of_return: str = typer.Option("10,14,18", help="Comma-separated list of annual rates of return in percentage"),
    years: int = typer.Option(25, help="Number of years for the investment"),
    show_invested: bool = typer.Option(False, help="Show invested amount in the plot. Might clutter the plot with many lines in case of multiple step-up values."),
    show_nominal: bool = typer.Option(False, help="Show nominal values in the plot. Useful for comparing with real values adjusted for inflation."),
    inflation_rate: float = typer.Option(0.0, help="Annual inflation rate in percentage"),
    colors: str = typer.Option(None, help="Comma-separated list of colors for the plots"),
    markers: str = typer.Option(None, help="Comma-separated list of markers for the plots"),
    save_as: str = typer.Option(None, help="File name to save the plot")
):
    """
    Plot the growth of investment portfolio over time with different SIP amounts, step-ups, and rates of return.
    """
    # Convert comma-separated strings to lists
    sip_amounts_list = [float(x) for x in sip_amounts.split(',')]
    step_ups_list = [float(x) for x in step_ups.split(',')]
    rates_of_return_list = [float(x) for x in rates_of_return.split(',')]
    colors_list = colors.split(',') if colors else None
    markers_list = markers.split(',') if markers else None
    
    num_rows = len(sip_amounts_list)
    num_cols = len(rates_of_return_list)
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 10))
    fig.tight_layout(pad=4.0)
    fig.suptitle(f'Investment Growth Over {years} Years with {inflation_rate}% Inflation\nInitial Lump Sum: INR {initial_lump_sum}', fontsize=12, fontstyle='italic')
    plt.subplots_adjust(top=0.9, hspace=0.4, wspace=0.4)
    
    if not colors_list:
        colors_list = ['c', 'm', 'y', 'k', 'r', 'g', 'b'][:len(step_ups_list)]
    if not markers_list:
        markers_list = ['o', 's', 'D', '^', 'v', 'p', 'P'][:len(step_ups_list)]
    
    color_cycle = itertools.cycle(colors_list)
    marker_cycle = itertools.cycle(markers_list)
    
    for i, sip in enumerate(sip_amounts_list):
        for j, rate in enumerate(rates_of_return_list):
            if num_cols > 1:
                ax = axs[i, j] if num_rows > 1 else axs[j]
            else:
                ax = axs[i] if num_rows > 1 else axs
            plt.sca(ax)
            title = f'SIP: {sip}, Rate: {rate}%'
            for step_up in step_ups_list:
                yearly_growth = calculate_yearly_growth(initial_lump_sum, sip, step_up, rate, years, inflation_rate)
                plot_growth(years, yearly_growth, title, color=next(color_cycle), marker=next(marker_cycle), label=f'Step-up: {step_up}%', show_invested=show_invested, show_nominal=show_nominal)
    if save_as:
        plt.savefig(save_as)
    
    plt.show()

@app.command()
def show_summary(
    initial_lump_sum: float = typer.Option(700000, help="Initial lump sum investment in INR"),
    sip_amounts: str = typer.Option("70000,120000,250000", help="Comma-separated list of SIP amounts in INR"),
    step_ups: str = typer.Option("0,10", help="Comma-separated list of annual step-up percentages"),
    rates_of_return: str = typer.Option("10,14,18", help="Comma-separated list of annual rates of return in percentage"),
    years: int = typer.Option(25, help="Number of years for the investment"),
    inflation_rate: float = typer.Option(0.0, help="Annual inflation rate in percentage"),
    save_as_csv: str = typer.Option(None, help="File name to save the summary as CSV")
):
    """
    Show a summary table of investment growth and optionally save it as a CSV file.
    """
    # Convert comma-separated strings to lists of floats
    sip_amounts_list = [float(x) for x in sip_amounts.split(',')]
    step_ups_list = [float(x) for x in step_ups.split(',')]
    rates_of_return_list = [float(x) for x in rates_of_return.split(',')]
    
    table = Table(title=f"Investment Growth Summary Over {years} Years with {inflation_rate}% Inflation\nInitial Lump Sum: INR {initial_lump_sum}")

    table.add_column("SIP Amount (INR)", justify="right")
    table.add_column("Step-up (%)", justify="right")
    table.add_column("Rate of Return (%)", justify="right")
    table.add_column(f"Invested Amount After {years} Years (INR Crore)", justify="right")
    table.add_column(f"Real Value After {years} Years (INR Crore)", justify="right")
    table.add_column(f"Nominal Value After {years} Years (INR Crore)", justify="right")

    rows = []
    for sip in sip_amounts_list:
        for step_up in step_ups_list:
            for rate in rates_of_return_list:
                yearly_data = calculate_yearly_growth(initial_lump_sum, sip, step_up, rate, years, inflation_rate)
                final = yearly_data[-1]
                rows.append([sip, step_up, rate, f"{final['invested_crore']:.2f}",f"{final['real_value_crore']:.2f}", f"{final['value_crore']:.2f}"])
                table.add_row(str(sip), str(step_up), str(rate),  f"{final['invested_crore']:.2f}",f"{final['real_value_crore']:.2f}", f"{final['value_crore']:.2f}")
    
    console.print(table)

    if save_as_csv:
        with open(save_as_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["SIP Amount (INR)", "Step-up (%)", "Rate of Return (%)", f"Real Value After {years} Years (INR Crore)", f"Invested Amount After {years} Years (INR Crore)"])
            writer.writerows(rows)

if __name__ == "__main__":
    app()

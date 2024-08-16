import matplotlib.pyplot as plt
import itertools
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

def calculate_yearly_growth(initial_lump_sum: float, monthly_sip: float, annual_step_up: float, annual_rate_of_return: float, years: int):
    monthly_rate_of_return = (1 + annual_rate_of_return / 100) ** (1/12) - 1
    yearly_values = []
    total_investment_value = initial_lump_sum

    for year in range(1, years + 1):
        current_sip = monthly_sip * ((1 + annual_step_up / 100) ** (year - 1))
        for month in range(12):
            total_investment_value += current_sip
            total_investment_value *= (1 + monthly_rate_of_return)
        yearly_values.append(total_investment_value / 1e7)
    
    return yearly_values

def plot_growth(years: int, yearly_growth: list[float], title: str, color: str = 'b', marker: str = 'o', label: str = None):
    years_list = list(range(1, years + 1))
    plt.plot(years_list, yearly_growth, marker=marker, linestyle='-', color=color, label=label)
    for i, value in enumerate(yearly_growth):
        plt.text(years_list[i], value, f'{value:.2f}', fontsize=8, ha='right')
    plt.title(title)
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value (INR Crore)')
    plt.grid(True)
    plt.legend()

@app.command()
def plot_multiple_growths(
    initial_lump_sum: float = typer.Option(700000, help="Initial lump sum investment in INR"),
    sip_amounts: str = typer.Option("70000,120000,250000", help="Comma-separated list of SIP amounts in INR"),
    step_ups: str = typer.Option("0,10,15", help="Comma-separated list of annual step-up percentages"),
    rates_of_return: str = typer.Option("10,14,18", help="Comma-separated list of annual rates of return in percentage"),
    years: int = typer.Option(25, help="Number of years for the investment"),
    colors: str = typer.Option(None, help="Comma-separated list of colors for the plots"),
    markers: str = typer.Option(None, help="Comma-separated list of markers for the plots"),
    save_as: str = typer.Option(None, help="File name to save the plot")
):
    """
    Plot the growth of investment portfolio over time with different SIP amounts, step-ups, and rates of return.
    """
    # Convert comma-separated strings to lists
    sip_amounts = [float(x) for x in sip_amounts.split(',')]
    step_ups = [float(x) for x in step_ups.split(',')]
    rates_of_return = [float(x) for x in rates_of_return.split(',')]
    colors = colors.split(',') if colors else None
    markers = markers.split(',') if markers else None
    
    num_rows = len(sip_amounts)
    num_cols = len(rates_of_return)
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 10))
    fig.tight_layout(pad=4.0)
    
    if not colors:
        colors = itertools.cycle(['c', 'm', 'y'])
    if not markers:
        markers = itertools.cycle(['o', 's', 'D'])
    
    for i, sip in enumerate(sip_amounts):
        for j, rate in enumerate(rates_of_return):
            ax = axs[i, j] if num_rows > 1 else axs[j]
            plt.sca(ax)
            title = f'SIP: {sip}, Rate: {rate}%'
            for step_up in step_ups:
                yearly_growth = calculate_yearly_growth(initial_lump_sum, sip, step_up, rate, years)
                plot_growth(years, yearly_growth, title, color=next(colors), marker=next(markers), label=f'Step-up: {step_up}%')
    
    if save_as:
        plt.savefig(save_as)
    
    plt.show()

@app.command()
def show_summary(
    initial_lump_sum: float = typer.Option(700000, help="Initial lump sum investment in INR"),
    sip_amounts: str = typer.Option("70000,120000,250000", help="Comma-separated list of SIP amounts in INR"),
    step_ups: str = typer.Option("0,10,15", help="Comma-separated list of annual step-up percentages"),
    rates_of_return: str = typer.Option("10,14,18", help="Comma-separated list of annual rates of return in percentage"),
    years: int = typer.Option(25, help="Number of years for the investment")
):
    """
    Show a summary table of investment growth.
    """
    # Convert comma-separated strings to lists of floats
    sip_amounts = [float(x) for x in sip_amounts.split(',')]
    step_ups = [float(x) for x in step_ups.split(',')]
    rates_of_return = [float(x) for x in rates_of_return.split(',')]
    
    table = Table(title="Investment Growth Summary")

    table.add_column("SIP Amount (INR)", justify="right")
    table.add_column("Step-up (%)", justify="right")
    table.add_column("Rate of Return (%)", justify="right")
    table.add_column(f"Value After {years} Years (INR Crore)", justify="right")

    for sip in sip_amounts:
        for step_up in step_ups:
            for rate in rates_of_return:
                yearly_growth = calculate_yearly_growth(initial_lump_sum, sip, step_up, rate, years)
                table.add_row(str(sip), str(step_up), str(rate), f"{yearly_growth[-1]:.2f}")
    
    console.print(table)

if __name__ == "__main__":
    app()

import matplotlib.pyplot as plt
import itertools

def calculate_yearly_growth(initial_lump_sum, monthly_sip, annual_step_up, annual_rate_of_return, years):
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

def plot_growth(years, yearly_growth, title, color='b', marker='o', label=None):
    years_list = list(range(1, years + 1))
    plt.plot(years_list, yearly_growth, marker=marker, linestyle='-', color=color, label=label)
    for i, value in enumerate(yearly_growth):
        plt.text(years_list[i], value, f'{value:.2f}', fontsize=8, ha='right')
    plt.title(title)
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value (INR Crore)')
    plt.grid(True)
    plt.legend()

def plot_multiple_growths(initial_lump_sum, sip_amounts, step_ups, rates_of_return, years, colors=None, markers=None, save_as=None):
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

# Given inputs
initial_lump_sum = 700000
sip_amounts = [70000, 120000, 250000]
step_ups = [0, 10, 15]
rates_of_return = [10, 14, 18]
years = 25

plot_multiple_growths(initial_lump_sum, sip_amounts, step_ups, rates_of_return, years, save_as='portfolio_growth.png')

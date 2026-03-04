import matplotlib
# non-interactive backend for batch runs
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def save_funding_plot(df, symbol: str, out_path: str):
    """Create and save a funding-rate plot from DataFrame to out_path.

    Expects `df` to have columns: `fundingTime`, `accumulatedFundingRate`, `fundingRate`.
    """
    if df is None or df.empty:
        # create an empty placeholder figure
        fig = plt.figure()
        fig.suptitle(f'No data for {symbol}')
        fig.savefig(out_path, bbox_inches='tight')
        plt.close(fig)
        return

    ax1 = df.plot(x='fundingTime', y='accumulatedFundingRate', ylabel='Accumulated Funding Rate', color='b', marker='o')
    ax2 = ax1.twinx()
    df.plot(x='fundingTime', y='fundingRate', ax=ax2, ylabel='Funding Rate', color='r', marker='x')
    plt.title(f'Funding Rate for {symbol}')
    ax1.legend(loc='upper left')
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close(fig)


import matplotlib.pyplot as plt
import io
import base64

def latex_to_png(formula: str, fontsize=7):
    """
    Convert LaTeX formula to base64 PNG for embedding in HTML.
    """
    fig, ax = plt.subplots(figsize=(0.1, 0.1))
    ax.text(
        0.1, 0.1,
        f"${formula}$",
        fontsize=fontsize,
        ha='center',
        va='center'
    )
    ax.axis('off')
    fig.tight_layout(pad=0)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=250, bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


### fix for equations
def latex_to_png_eq(formula: str, fontsize=7):
    """
    Convert LaTeX formula to base64 PNG for embedding in HTML.
    """
    fig, ax = plt.subplots(figsize=(0.1, 0.1))
    ax.text(
        0.1, 0.1,
        f"${formula}$",
        fontsize=fontsize,
        ha='center',
        va='center'
    )
    ax.axis('off')
    fig.tight_layout(pad=0)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=250, bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

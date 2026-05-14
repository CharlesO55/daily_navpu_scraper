def color_metric(val):
    if not val:
        color = 'gray'
    elif val > 0:
        color = '#09ab3b' # Streamlit metric green
    elif val < 0:
        color = '#ff2b2b' # Streamlit metric red
    else:
        color = 'gray'
    return f'color: {color}'


def format_metric(val):
    if not val:
        return "▬"
    elif val > 0:
        return f"▲ {val:.2%}"
    elif val < 0:
        return f"▼ {abs(val):.2%}"
    return f"▬ {val}"
from quanttools.utils import calc_max_drawdown


def test_max_drawdown():
    eq = [100, 120, 110, 130, 90]
    dd = calc_max_drawdown(eq)
    # (130 - 90) / 130 = 0.307692...
    assert round(dd, 6) == round((130 - 90) / 130, 6)

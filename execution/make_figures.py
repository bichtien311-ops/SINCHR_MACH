"""
Генерация иллюстраций для курса «Синхронные машины».

Создаёт PNG-рисунки (векторные диаграммы, характеристики) в папке
Синхронные_машины/figures/. Эти рисунки вставляются в лекции и методичку
через markdown-синтаксис ![подпись](../figures/имя.png).

Запуск:
    python execution/make_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "Синхронные_машины" / "figures"

plt.rcParams.update({
    "figure.dpi": 130,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.titlesize": 12,
})


def save(fig, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / name
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  + {name}")


def fig_l01_speed() -> None:
    """Синхронная частота вращения от числа пар полюсов."""
    p = np.arange(1, 13)
    n = 60 * 50 / p
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.plot(p, n, "o-", color="#1f6feb")
    for xi, yi in zip(p, n):
        if xi in (1, 2, 4, 6, 12):
            ax.annotate(f"{int(yi)}", (xi, yi), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=9)
    ax.set_xlabel("Число пар полюсов p")
    ax.set_ylabel("n, об/мин")
    ax.set_title("Синхронная частота вращения, f = 50 Гц")
    save(fig, "l01_speed.png")


def fig_l03_emf() -> None:
    """ЭДС: синусоида и влияние 5-й гармоники."""
    t = np.linspace(0, 2 * np.pi, 500)
    e1 = np.sin(t)
    e5 = 0.2 * np.sin(5 * t)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(t, e1, label="основная гармоника", color="#1f6feb")
    ax.plot(t, e1 + e5, label="с 5-й гармоникой", color="#d1242f", lw=1)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("ωt, рад")
    ax.set_ylabel("e / E_m")
    ax.set_title("Форма ЭДС и высшая гармоника")
    ax.legend(fontsize=9, loc="upper right")
    save(fig, "l03_emf.png")


def fig_l05_occ_scc() -> None:
    """Характеристики холостого хода (с насыщением) и КЗ (линейная)."""
    iv = np.linspace(0, 1.2, 100)
    occ = 1.1 * (1 - np.exp(-2.4 * iv))          # насыщающаяся ХХХ
    occ_lin = 0.95 * iv                           # касательная (ненасыщ.)
    scc = 0.9 * iv                                # линейная ХКЗ
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(iv, occ, color="#1f6feb", label="ХХХ  E₀(I_в)")
    ax.plot(iv, occ_lin, "--", color="#1f6feb", lw=1, label="ХХХ (ненасыщ.)")
    ax.plot(iv, scc, color="#d1242f", label="ХКЗ  I_к(I_в)")
    ax.set_xlabel("Ток возбуждения I_в, о.е.")
    ax.set_ylabel("E₀ , I_к (о.е.)")
    ax.set_title("Характеристики ХХ и КЗ")
    ax.legend(fontsize=9)
    save(fig, "l05_occ_scc.png")


def _phasor(ax, start, vec, color, label, lw=2):
    ax.annotate("", xy=(start[0] + vec[0], start[1] + vec[1]), xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw))
    mid = (start[0] + vec[0] / 2, start[1] + vec[1] / 2)
    ax.text(mid[0], mid[1], label, color=color, fontsize=10,
            ha="center", va="bottom")


def fig_l05_vector() -> None:
    """Векторная диаграмма неявнополюсного генератора (инд. нагрузка)."""
    U = np.array([3.5, 0.0])
    phi = np.deg2rad(36.87)
    I = 1.6 * np.array([np.cos(-phi), np.sin(-phi)])
    jIX = np.array([-(-1.6 * np.sin(-phi)) * 0 + 1.6 * 0, 0])  # placeholder
    # jIXd опережает ток на 90°
    Ixd = 2.0
    dir_I = I / np.linalg.norm(I)
    jdir = np.array([-dir_I[1], dir_I[0]])
    jIX = Ixd * jdir
    E0 = U + jIX
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    _phasor(ax, (0, 0), U, "#1f6feb", "U")
    _phasor(ax, (0, 0), I * 1.2, "#2da44e", "I")
    _phasor(ax, U, jIX, "#bf8700", "jIX_d")
    _phasor(ax, (0, 0), E0, "#d1242f", "E₀")
    ax.text(E0[0] * 0.45, E0[1] * 0.6 + 0.15, "θ", fontsize=12)
    lim = 6
    ax.set_xlim(-1, lim)
    ax.set_ylim(-2, lim - 1)
    ax.set_aspect("equal")
    ax.set_title("Векторная диаграмма генератора (инд. нагрузка)")
    save(fig, "l05_vector.png")


def fig_l06_salient() -> None:
    """Сравнение синхронных реактивностей X_d и X_q (полярная форма зазора)."""
    theta = np.linspace(0, 2 * np.pi, 400)
    xd, xq = 1.0, 0.6
    r = xq + (xd - xq) * np.abs(np.cos(theta))
    fig, ax = plt.subplots(figsize=(4.8, 4.4), subplot_kw={"projection": "polar"})
    ax.plot(theta, r, color="#1f6feb")
    ax.set_title("Магнитная проводимость: ось d (макс.) и q (мин.)", pad=18, fontsize=10)
    save(fig, "l06_salient.png")


def fig_l07_external() -> None:
    """Внешние характеристики при разных cos φ."""
    I = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(I, 1 - 0.45 * I, color="#d1242f", label="инд. (0.8)")
    ax.plot(I, 1 - 0.18 * I, color="#1f6feb", label="актив. (1.0)")
    ax.plot(I, 1 + 0.12 * I, color="#2da44e", label="ёмк. (0.8)")
    ax.set_xlabel("Ток нагрузки I / I_ном")
    ax.set_ylabel("U / U_ном")
    ax.set_title("Внешние характеристики U(I), I_в = const")
    ax.legend(fontsize=9)
    save(fig, "l07_external.png")


def fig_l09_angle() -> None:
    """Угловая характеристика: неявнополюсная и явнополюсная машины."""
    th = np.linspace(0, np.pi, 400)
    deg = np.rad2deg(th)
    p_round = np.sin(th)
    p_react = 0.3 * np.sin(2 * th)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(deg, p_round, color="#1f6feb", label="неявнополюсная: sin θ")
    ax.plot(deg, p_round + p_react, color="#d1242f",
            label="явнополюсная: + рект. (sin 2θ)")
    ax.plot(deg, p_react, "--", color="#bf8700", lw=1, label="реактивная сост.")
    ax.axvline(90, color="k", lw=0.6, ls=":")
    ax.set_xlabel("Угол нагрузки θ, °")
    ax.set_ylabel("P / P_max")
    ax.set_title("Угловая характеристика P(θ)")
    ax.legend(fontsize=8.5)
    save(fig, "l09_angle.png")


def fig_l10_ucurves() -> None:
    """U-образные характеристики тока статора от возбуждения."""
    iv = np.linspace(0.5, 1.5, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for P, c, lbl in [(0.2, "#2da44e", "P = 0.2"),
                      (0.5, "#1f6feb", "P = 0.5"),
                      (0.8, "#d1242f", "P = 0.8")]:
        ia = np.sqrt(P**2 + (2.2 * (iv - 1.0))**2) + 0.05
        ax.plot(iv, ia, color=c, label=lbl)
    ax.axvline(1.0, color="k", lw=0.6, ls=":")
    ax.text(1.0, 0.05, "cos φ = 1", fontsize=8, ha="center")
    ax.set_xlabel("Ток возбуждения I_в, о.е.")
    ax.set_ylabel("Ток статора I_a, о.е.")
    ax.set_title("U-образные характеристики I_a(I_в)")
    ax.legend(fontsize=9)
    save(fig, "l10_ucurves.png")


def fig_l11_motor() -> None:
    """Угловая характеристика двигателя: устойчивая и неустойчивая зоны."""
    th = np.linspace(0, np.pi, 400)
    deg = np.rad2deg(th)
    M = np.sin(th)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(deg, M, color="#1f6feb")
    ax.fill_between(deg, M, where=(deg <= 90), color="#2da44e", alpha=0.15,
                    label="устойчиво (θ<90°)")
    ax.fill_between(deg, M, where=(deg >= 90), color="#d1242f", alpha=0.15,
                    label="неустойчиво (θ>90°)")
    ax.axvline(90, color="k", lw=0.6, ls=":")
    ax.set_xlabel("Угол нагрузки θ, °")
    ax.set_ylabel("M / M_max")
    ax.set_title("Момент двигателя M(θ) и устойчивость")
    ax.legend(fontsize=9)
    save(fig, "l11_motor.png")


def fig_l12_short() -> None:
    """Ток внезапного КЗ: затухающая огибающая."""
    t = np.linspace(0, 0.5, 1000)
    env = 1 + 7 * np.exp(-t / 0.03) + 1.5 * np.exp(-t / 0.15)
    i = env * np.sin(2 * np.pi * 50 * t)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.plot(t, i, color="#1f6feb", lw=0.7)
    ax.plot(t, env, "--", color="#d1242f", lw=1.2, label="огибающая")
    ax.plot(t, -env, "--", color="#d1242f", lw=1.2)
    ax.set_xlabel("t, с")
    ax.set_ylabel("i_к, о.е.")
    ax.set_title("Ток внезапного КЗ: X″_d → X′_d → X_d")
    ax.legend(fontsize=9)
    save(fig, "l12_short.png")


def main() -> None:
    print(f"Рисунки: {FIG_DIR}")
    fig_l01_speed()
    fig_l03_emf()
    fig_l05_occ_scc()
    fig_l05_vector()
    fig_l06_salient()
    fig_l07_external()
    fig_l09_angle()
    fig_l10_ucurves()
    fig_l11_motor()
    fig_l12_short()
    print("Готово.")


if __name__ == "__main__":
    main()

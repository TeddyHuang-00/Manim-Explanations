import manim as mm
import numpy as np
from scipy.optimize import curve_fit
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import RBF

np.random.seed(1234)


class Regression(mm.Scene):
    def construct(self):
        title = mm.Text("回归", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        number_plane = mm.NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={"include_tip": False},
        )
        self.play(mm.Create(number_plane))
        self.wait(1)

        x = np.random.uniform(-5, 5, 100)
        y = x / 2 + 1 + np.random.normal(0, 0.5, 100)
        line = mm.Line(
            number_plane.coords_to_point(-5, -5 / 2 + 1),
            number_plane.coords_to_point(5, 5 / 2 + 1),
            color=mm.RED,
        )
        number_plane.add(line)
        self.play(mm.Create(line))
        formula = mm.MathTex(R"{{ y }}={{ a }}{{ x }}+{{ b }}").next_to(
            number_plane, mm.LEFT
        )
        self.play(
            mm.Write(formula),
            mm.VGroup(number_plane, formula).animate.center(),
        )
        self.wait(1)

        self.play(
            formula.animate.set_color_by_tex(" a ", mm.RED).set_color_by_tex(
                " b ", mm.BLUE
            )
        )
        self.wait(1)

        self.play(
            mm.Indicate(formula.get_part_by_tex(" y ")),  # type: ignore
            mm.Indicate(formula.get_part_by_tex(" x ")),  # type: ignore
        )
        self.wait(1)

        points = mm.VGroup(
            *[
                mm.Dot(number_plane.c2p(x[i], y[i]), color=mm.RED, fill_opacity=0.75)
                for i in range(len(x))
            ]
        )
        self.play(mm.FadeOut(line), mm.Create(points))
        number_plane.remove(line)
        self.play(
            mm.Transform(
                formula,
                mm.MathTex(R"{{ y }}={{ a }}{{ x }}+{{ b }}+{{ \varepsilon }}")
                .next_to(number_plane, mm.LEFT)
                .set_color_by_tex(" a ", mm.RED)
                .set_color_by_tex(" b ", mm.BLUE)
                .set_color_by_tex(R" \varepsilon ", mm.YELLOW),
            )
        )
        self.wait(1)

        a = mm.ValueTracker(1)
        b = mm.ValueTracker(0)
        fitted = number_plane.plot(
            lambda x: a.get_value() * x + b.get_value(), color=mm.WHITE
        )
        fitted.add_updater(
            lambda m: m.become(
                number_plane.plot(
                    lambda x: a.get_value() * x + b.get_value(), color=mm.WHITE
                )
            )  # type: ignore
        )
        self.play(mm.Create(fitted))
        self.play(
            mm.Transform(
                formula,
                mm.MathTex(R"{{ \hat{y} }}={{ a }}{{ x }}+{{ b }}")
                .next_to(number_plane, mm.LEFT)
                .set_color_by_tex(" a ", mm.RED)
                .set_color_by_tex(" b ", mm.BLUE),
            ),
        )
        self.wait(1)

        a_label = mm.MathTex("{{ a }}=").set_color_by_tex(" a ", mm.RED)
        a_num = mm.DecimalNumber(a.get_value(), num_decimal_places=2).next_to(
            a_label, mm.RIGHT
        )
        mm.VGroup(a_label, a_num).next_to(formula, mm.DOWN)
        b_label = mm.MathTex("{{ b }}=").set_color_by_tex(" b ", mm.BLUE)
        b_num = mm.DecimalNumber(b.get_value(), num_decimal_places=2).next_to(
            b_label, mm.RIGHT
        )
        mm.VGroup(b_label, b_num).next_to(mm.VGroup(a_label, a_num), mm.DOWN).align_to(
            mm.VGroup(a_label, a_num), mm.LEFT
        )
        a_num.add_updater(
            lambda m: m.set_value(a.get_value()).next_to(a_label, mm.RIGHT)
        )
        b_num.add_updater(
            lambda m: m.set_value(b.get_value()).next_to(b_label, mm.RIGHT)
        )
        self.play(mm.Write(mm.VGroup(a_label, a_num, b_label, b_num)))
        self.wait(1)

        self.play(
            a.animate.set_value(0.5),
            b.animate.set_value(1.5),
        )
        self.wait(1)

        self.play(
            a.animate.set_value(2),
            b.animate.set_value(0),
        )
        self.wait(1)

        self.play(
            a.animate.set_value(0.5),
            b.animate.set_value(1),
        )
        self.play(
            mm.ShowPassingFlash(
                fitted.copy().set_color(mm.GREEN),  # type: ignore
            )
        )
        self.wait(1)

        y_nonlinear = 2 * np.tanh(x) + np.random.normal(0, 0.5, 100)
        points_nonlinear = mm.VGroup(
            *[
                mm.Dot(
                    number_plane.c2p(x[i], y_nonlinear[i]),
                    color=mm.RED,
                    fill_opacity=0.75,
                )
                for i in range(len(x))
            ]
        )
        self.play(mm.ReplacementTransform(points, points_nonlinear))
        self.wait(1)

        self.play(
            a.animate.set_value(0.5),
            b.animate.set_value(0),
        )
        self.wait(1)

        self.play(
            a.animate.set_value(2),
            b.animate.set_value(0),
        )
        self.wait(1)

        self.play(
            a.animate.set_value(0),
            b.animate.set_value(2),
        )
        self.wait(1)

        question = mm.Text("?").scale(3)
        self.remove(*[mob for mob in self.mobjects if mob != title])
        self.wait(1)

        self.play(mm.Write(question))
        self.play(mm.Wiggle(question))
        self.wait(1)

        self.play(*[mm.FadeOut(mob) for mob in self.mobjects])
        self.wait(1)


class Reverse(mm.Scene):
    def construct(self):
        N = 50

        title = mm.Text("建模", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        arrow = mm.Arrow(mm.ORIGIN, mm.RIGHT * 2).center()
        model_text = mm.Text("模型").next_to(arrow, mm.LEFT)
        data_text = mm.Text("数据").next_to(arrow, mm.RIGHT)
        self.play(mm.Create(arrow), mm.Write(model_text), mm.Write(data_text))
        self.wait(1)

        model = (
            mm.MathTex(R"{{ y }}=f({{ x }})+{{ \varepsilon }}")
            .set_color_by_tex(R" \varepsilon ", mm.YELLOW)
            .next_to(arrow, mm.LEFT)
        )
        axes = mm.Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False},
        ).next_to(arrow, mm.RIGHT)
        x = np.random.uniform(-2, 2, N)
        y = x / 2 + np.sin(x * 3 * np.pi) / 2 + np.random.normal(0, 0.1, N)
        points = mm.VGroup(
            *[
                mm.Dot(axes.c2p(x[i], y[i]), color=mm.RED, fill_opacity=0.8)
                for i in range(N)
            ]
        )
        self.play(mm.ReplacementTransform(model_text, model))
        self.wait(1)
        self.play(mm.ReplacementTransform(data_text, axes))
        self.play(mm.Create(points))
        self.wait(1)

        model_backwards = mm.MathTex(R"{{ \hat{y} }}=g({{ x }})").next_to(
            arrow, mm.LEFT
        )
        text_backwards = mm.Text("反向建模").next_to(arrow, mm.UP)
        self.play(
            mm.Write(text_backwards),
            arrow.animate.rotate(mm.PI),
            mm.ReplacementTransform(model, model_backwards),
        )
        self.wait(1)

        axes.add(points)
        model_linear = (
            mm.MathTex(R"{{ \hat{y} }}={{ a }}{{ x }}+{{ b }}")
            .set_color_by_tex(" a ", mm.GREEN)
            .set_color_by_tex(" b ", mm.GREEN)
            .move_to(mm.LEFT * 3)
        )
        self.play(
            axes.animate.scale(1.5).to_edge(mm.RIGHT), mm.FadeOut(text_backwards, arrow)
        )

        func_linear = lambda x: x / 2
        plot_linear = axes.plot(func_linear)
        self.play(
            mm.ReplacementTransform(model_backwards, model_linear),
            mm.Create(plot_linear),
        )
        self.wait(1)

        error_linear = mm.VGroup(
            *[
                mm.Line(
                    axes.c2p(x[i], y[i]),
                    axes.c2p(x[i], func_linear(x[i])),
                    color=mm.YELLOW,
                )
                for i in range(N)
            ]
        )
        self.play(mm.Create(error_linear))
        self.wait(1)
        self.play(mm.FadeOut(error_linear))
        self.wait(1)

        func_nonlinear = lambda x: x / 2 + np.sin(x * 3 * np.pi) / 2
        model_nonlinear = (
            mm.MathTex(
                R"{{ \hat{y} }}={{ a }}{{ x }}+{{ b }}\sin({{ \omega }}{{ x }})+{{ c }}"
            )
            .set_color_by_tex(" a ", mm.GREEN)
            .set_color_by_tex(" b ", mm.GREEN)
            .set_color_by_tex(R" \omega ", mm.GREEN)
            .set_color_by_tex(" c ", mm.GREEN)
            .move_to(mm.LEFT * 3)
        )
        plot_nonlinear = axes.plot(func_nonlinear)
        self.play(
            mm.ReplacementTransform(model_linear, model_nonlinear),
            mm.ReplacementTransform(plot_linear, plot_nonlinear),
        )
        self.wait(1)

        error_nonlinear = mm.VGroup(
            *[
                mm.Line(
                    axes.c2p(x[i], y[i]),
                    axes.c2p(x[i], func_nonlinear(x[i])),
                    color=mm.YELLOW,
                )
                for i in range(N)
            ]
        )
        self.play(mm.Create(error_nonlinear))
        self.wait(1)
        self.play(mm.FadeOut(error_nonlinear))
        self.wait(1)

        self.play(mm.ShowPassingFlash(plot_nonlinear.copy().set_color(mm.GREEN)))  # type: ignore
        self.wait(1)

        L = 24
        xx = np.linspace(-2, 2, L)
        yy = func_nonlinear(xx)
        l = [
            lambda x, i=i: np.prod(x - xx[:i])
            * np.prod(x - xx[i + 1 :])
            / (np.prod(xx[i] - xx[:i]) * np.prod(xx[i] - xx[i + 1 :]))
            for i in range(L)
        ]
        func_nonlinear_lagrange = lambda x: sum([l[i](x) * yy[i] for i in range(L)])
        model_nonlinear_lagrange = (
            mm.MathTex(R"{{ \hat{y} }}={{ k_0 }}+{{ k_1 }}x+{{ k_2 }}x^2+{{ \cdots }}")
            .set_color_by_tex(" k_0 ", mm.GREEN)
            .set_color_by_tex(" k_1 ", mm.GREEN)
            .set_color_by_tex(" k_2 ", mm.GREEN)
            .move_to(mm.LEFT * 3)
        )
        plot_nonlinear_lagrange = axes.plot(func_nonlinear_lagrange)
        self.play(
            mm.ReplacementTransform(model_nonlinear, model_nonlinear_lagrange),
            mm.ReplacementTransform(plot_nonlinear, plot_nonlinear_lagrange),
        )
        self.wait(1)


class Derivation(mm.Scene):
    def construct(self):
        CMAP = {
            " E ": mm.RED,
            " E_0 ": mm.RED,
            " a ": mm.RED,
            " S ": mm.BLUE,
            " S_0 ": mm.BLUE,
            " b ": mm.BLUE,
            " ES ": mm.PURPLE,
            " P ": mm.GREEN,
        }
        title = mm.Text("正向建模", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        arrow_R = mm.Arrow(mm.ORIGIN, mm.RIGHT * 2).center()
        model_text = mm.Text("模型").next_to(arrow_R, mm.LEFT)
        data_text = mm.Text("数据").next_to(arrow_R, mm.RIGHT)
        self.play(mm.Create(arrow_R), mm.Write(model_text), mm.Write(data_text))
        self.wait(1)

        arrow_L = mm.Arrow(mm.ORIGIN, mm.RIGHT * 2).next_to(model_text, mm.LEFT)
        theory = mm.Text("理论").next_to(arrow_L, mm.LEFT)
        self.play(
            mm.Create(arrow_L),
            mm.Write(theory),
            mm.VGroup(theory, arrow_L, model_text, arrow_R, data_text).animate.center(),
        )
        self.wait(1)

        self.play(
            mm.FadeOut(arrow_R, data_text),
            mm.VGroup(arrow_L, theory, model_text).animate.center().scale(1.5),
        )
        self.wait(1)

        enzyme_kinetics_text = mm.Text("酶动力学").next_to(arrow_L, mm.LEFT)
        concentration_text = mm.Text("产物浓度").next_to(arrow_L, mm.RIGHT)
        self.play(
            mm.ReplacementTransform(theory, enzyme_kinetics_text),
            mm.ReplacementTransform(model_text, concentration_text),
        )
        self.wait(1)

        self.play(mm.FadeOut(enzyme_kinetics_text, arrow_L, concentration_text))
        self.wait(1)

        enzyme_zh_text = mm.Text("酶").scale(1.5)
        enzyme_en_text = mm.Text("Enzyme").next_to(enzyme_zh_text, mm.DOWN)
        mm.VGroup(enzyme_zh_text, enzyme_en_text).center()
        self.play(mm.Write(enzyme_zh_text))
        self.play(mm.Write(enzyme_en_text))
        self.wait(1)

        enzyme = (
            mm.MathTex("{{ E }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
            .next_to(enzyme_en_text, mm.UP)
        )
        self.play(mm.ReplacementTransform(enzyme_zh_text, enzyme))
        self.wait(1)

        enzyme.generate_target()
        enzyme.target.scale(0.5).to_edge(mm.RIGHT)  # type: ignore
        self.play(mm.FadeOut(enzyme_en_text), mm.MoveToTarget(enzyme))
        self.wait(1)

        substrate_zh_text = mm.Text("底物").scale(1.5)
        substrate_en_text = mm.Text("Substrate").next_to(substrate_zh_text, mm.DOWN)
        mm.VGroup(substrate_zh_text, substrate_en_text).center()
        self.play(mm.Write(substrate_zh_text))
        self.play(mm.Write(substrate_en_text))
        self.wait(1)

        substrate = (
            mm.MathTex("{{ S }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
            .next_to(substrate_en_text, mm.UP)
        )
        self.play(mm.ReplacementTransform(substrate_zh_text, substrate))
        self.wait(1)

        substrate.generate_target()
        substrate.target.scale(0.5)  # type: ignore
        (
            mm.VGroup(enzyme.target, substrate.target)
            .arrange(mm.DOWN)  # type: ignore
            .to_edge(mm.RIGHT)
        )
        self.play(
            mm.FadeOut(substrate_en_text),
            mm.MoveToTarget(enzyme),
            mm.MoveToTarget(substrate),
        )
        self.wait(1)

        complex_zh_text = mm.Text("酶-底物复合物").scale(1.5)
        complex_en_text = mm.Text("Enzyme-Substrate Complex").next_to(
            complex_zh_text, mm.DOWN
        )
        mm.VGroup(complex_zh_text, complex_en_text).center()
        self.play(mm.Write(complex_zh_text))
        self.play(mm.Write(complex_en_text))
        self.wait(1)

        complex = (
            mm.MathTex("{{ ES }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
            .next_to(complex_en_text, mm.UP)
        )
        self.play(mm.ReplacementTransform(complex_zh_text, complex))
        self.wait(1)

        complex.generate_target()
        complex.target.scale(0.5)  # type: ignore
        (
            mm.VGroup(enzyme.target, substrate.target, complex.target)
            .arrange(mm.DOWN)  # type: ignore
            .to_edge(mm.RIGHT)
        )
        self.play(
            mm.FadeOut(complex_en_text),
            mm.MoveToTarget(enzyme),
            mm.MoveToTarget(substrate),
            mm.MoveToTarget(complex),
        )
        self.wait(1)

        product_zh_text = mm.Text("产物").scale(1.5)
        product_en_text = mm.Text("Product").next_to(product_zh_text, mm.DOWN)
        mm.VGroup(product_zh_text, product_en_text).center()
        self.play(mm.Write(product_zh_text))
        self.play(mm.Write(product_en_text))
        self.wait(1)

        product = (
            mm.MathTex("{{ P }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
            .next_to(product_en_text, mm.UP)
        )
        self.play(mm.ReplacementTransform(product_zh_text, product))
        self.wait(1)

        product.generate_target()
        product.target.scale(0.5)  # type: ignore
        (
            mm.VGroup(enzyme.target, substrate.target, complex.target, product.target)
            .arrange(mm.DOWN)  # type: ignore
            .to_edge(mm.RIGHT)
        )
        self.play(
            mm.FadeOut(product_en_text),
            mm.MoveToTarget(enzyme),
            mm.MoveToTarget(substrate),
            mm.MoveToTarget(complex),
            mm.MoveToTarget(product),
        )
        self.wait(1)

        formula = (
            mm.MathTex(
                R"{{ E }}+{{ S }}\rightleftharpoons{{ ES }}\rightleftharpoons{{ E }}+{{ P }}"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(
            mm.ReplacementTransform(
                mm.VGroup(enzyme, enzyme.copy(), substrate, complex, product), formula
            )
        )
        self.wait(1)

        harpoon_L = formula.get_parts_by_tex(R"\rightleftharpoons")[0]
        harpoon_R = formula.get_parts_by_tex(R"\rightleftharpoons")[1]
        k1f = mm.MathTex(R"{{ k_{1} }}").next_to(harpoon_L, mm.UP)
        k1r = mm.MathTex(R"{{ k_{-1} }}").next_to(harpoon_L, mm.DOWN)
        k2f = mm.MathTex(R"{{ k_{2} }}").next_to(harpoon_R, mm.UP)
        k2r = mm.MathTex(R"{{ k_{-2} }}").next_to(harpoon_R, mm.DOWN)
        self.play(mm.Indicate(harpoon_L))
        self.play(mm.Write(k1f))
        self.play(mm.Write(k1r))
        self.play(mm.Indicate(harpoon_R))
        self.play(mm.Write(k2f))
        self.play(mm.Write(k2r))
        self.wait(1)

        non_reversible_text = mm.Text("不可逆假设").move_to(mm.UP * 2)
        formula_no_k2r = (
            mm.MathTex(
                R"{{ E }}+{{ S }}\rightleftharpoons{{ ES }}\rightharpoonup{{ E }}+{{ P }}"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.Write(non_reversible_text))
        self.play(
            mm.ReplacementTransform(formula, formula_no_k2r),
            mm.FadeOut(k2r),
        )
        self.wait(1)

        stasis_text = mm.Text("稳态假设").move_to(mm.UP * 2)
        equation = (
            mm.MathTex(
                R"{{ ( }}{{ k_{-1} }}+{{ k_{2} }}{{ ) }}{{ [ }}{{ ES }}{{ ] }}={{ k_{1} }}{{ [ }}{{ E }}{{ ] }}{{ [ }}{{ S }}{{ ] }}"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(non_reversible_text, stasis_text))
        self.play(
            mm.VGroup(formula_no_k2r, k1f, k1r, k2f).animate.scale(0.7).to_edge(mm.DOWN)
        )
        self.play(mm.Write(equation))
        self.wait(1)

        self.play(
            mm.Indicate(equation.get_parts_by_tex(R" k_{1} ")),
            mm.Indicate(equation.get_parts_by_tex(R" E ")),
            mm.Indicate(equation.get_parts_by_tex(R" S ")),
        )
        self.wait(1)

        self.play(
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" E ")[0]),
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" S ")),
        )
        self.play(mm.Indicate(k1f))
        self.play(mm.Indicate(formula_no_k2r.get_parts_by_tex(R" ES ")))
        self.wait(1)

        self.play(
            mm.Indicate(equation.get_parts_by_tex(R" k_{-1} ")),
            mm.Indicate(equation.get_parts_by_tex(R" k_{2} ")),
            mm.Indicate(equation.get_parts_by_tex(R" ES ")),
        )
        self.wait(1)

        self.play(mm.Indicate(formula_no_k2r.get_parts_by_tex(R" ES ")))
        self.play(mm.Indicate(k1r))
        self.play(
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" E ")[0]),
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" S ")),
        )
        self.play(mm.Indicate(formula_no_k2r.get_parts_by_tex(R" ES ")))
        self.play(mm.Indicate(k2f))
        self.play(
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" E ")[1]),
            mm.Indicate(formula_no_k2r.get_parts_by_tex(R" P ")),
        )
        self.wait(1)

        self.play(
            mm.Indicate(equation.get_parts_by_tex(R" [ ")[0]),
            mm.Indicate(equation.get_parts_by_tex(R" ] ")[0]),
            mm.Indicate(equation.get_parts_by_tex(R" [ ")[1]),
            mm.Indicate(equation.get_parts_by_tex(R" ] ")[1]),
            mm.Indicate(equation.get_parts_by_tex(R" [ ")[2]),
            mm.Indicate(equation.get_parts_by_tex(R" ] ")[2]),
        )
        self.wait(1)

        equation_ES = (
            mm.MathTex(R"[{{ ES }}]={ k_{1} \over k_{-1}+k_{2} }[{{ E }}][{{ S }}]")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.Indicate(equation.get_parts_by_tex(R" ES ")))
        self.play(mm.ReplacementTransform(equation, equation_ES))
        self.wait(1)

        approximation_text = mm.Text("近似假设")
        approximation_eq = (
            mm.MathTex(R"[{{ E }}]={{ E_0 }}-[{{ ES }}]\approx {{ E_0 }}")
            .set_color_by_tex_to_color_map(CMAP)
            .next_to(approximation_text, mm.RIGHT)
        )
        mm.VGroup(approximation_text, approximation_eq).center().move_to(mm.UP * 2)
        self.play(mm.ReplacementTransform(stasis_text, approximation_text))
        self.play(mm.Write(approximation_eq))
        self.wait(1)

        equation_constant_E = (
            mm.MathTex(R"[{{ ES }}]={ k_{1} \over k_{-1}+k_{2} }{{ E_0 }}[{{ S }}]")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(
            mm.LaggedStart(
                mm.FocusOn(equation_ES.get_parts_by_tex(" E "), run_time=1),
                mm.FadeTransform(equation_ES, equation_constant_E),
                lag_ratio=0.5,
            ),
        )
        self.wait(1)

        conservation_text = mm.Text("质量守恒")
        conservation_eq = (
            mm.MathTex(R"[{{ S }}]\approx {{ S_0 }}-[{{ P }}]")
            .set_color_by_tex_to_color_map(CMAP)
            .next_to(conservation_text, mm.RIGHT)
        )
        mm.VGroup(conservation_text, conservation_eq).center().move_to(mm.UP * 2)
        self.play(
            mm.ReplacementTransform(approximation_text, conservation_text),
            mm.ReplacementTransform(approximation_eq, conservation_eq),
        )
        self.wait(1)

        equation_conserve_S = (
            mm.MathTex(
                R"[{{ ES }}]={ k_{1} \over k_{-1}+k_{2} }{{ E_0 }}({{ S_0 }}-[{{ P }}])"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(
            mm.LaggedStart(
                mm.FocusOn(
                    mm.VGroup(
                        equation_conserve_S.get_parts_by_tex(" S_0 "),
                        equation_conserve_S.get_parts_by_tex(" P "),
                    ),
                    run_time=1,
                ),
                mm.FadeTransform(equation_constant_E, equation_conserve_S),
                lag_ratio=0.5,
            ),
        )
        self.wait(1)

        product_text = mm.Text("产物生成")
        product_eq = (
            mm.MathTex(R"{ d[{{ P }}] \over dt }=k_{2}[{{ ES }}]")
            .set_color_by_tex_to_color_map(CMAP)
            .next_to(product_text, mm.RIGHT)
        )
        mm.VGroup(product_text, product_eq).center().move_to(mm.UP * 2)
        self.play(
            mm.ReplacementTransform(conservation_text, product_text),
            mm.ReplacementTransform(conservation_eq, product_eq),
        )

        self.play(mm.Indicate(formula_no_k2r.get_parts_by_tex(R" ES ")))
        self.play(mm.Indicate(k2f))
        self.play(mm.Indicate(formula_no_k2r.get_parts_by_tex(R" P ")))
        self.wait(1)

        equation_product = (
            mm.MathTex(
                R"{ d[{{ P }}] \over dt }={ k_{1}k_2 \over k_{-1}+k_{2} }{{ E_0 }}({{ S_0 }}-[{{ P }}])"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.FadeTransformPieces(equation_conserve_S, equation_product))
        self.wait(1)

        equation_product_final = (
            mm.MathTex(R"{ d[{{ P }}] \over dt }={{ K }}{{ E_0 }}({{ S_0 }}-[{{ P }}])")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(
            mm.LaggedStart(
                mm.FocusOn(equation_product, run_time=1),
                mm.FadeTransform(equation_product, equation_product_final),
                lag_ratio=0.5,
            ),
        )
        self.wait(1)

        notation = mm.MathTex(R"K={ k_{1}k_2 \over k_{-1}+k_{2} }").to_edge(mm.DOWN)
        self.play(
            mm.ReplacementTransform(mm.VGroup(formula_no_k2r, k1f, k1r, k2f), notation)
        )
        self.wait(1)

        transpose_text = mm.Text("移项").move_to(mm.UP * 2)
        self.play(
            mm.ReplacementTransform(mm.VGroup(product_text, product_eq), transpose_text)
        )
        self.wait(1)

        equation_transposed = (
            mm.MathTex(
                R"{ d[{{ P }}] \over {{ S_0 }}-[{{ P }}] }={{ K }}{{ E_0 }}\cdot{{ dt }}"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(equation_product_final, equation_transposed))
        self.wait(1)

        integrate_text = mm.Text("积分").move_to(mm.UP * 2)
        self.play(mm.ReplacementTransform(transpose_text, integrate_text))
        self.wait(1)

        equation_integrated = (
            mm.MathTex(
                R"\ln{ 1 \over 1-{ [{{ P }}] \over {{ S_0 }} } }={{ K }}{{ E_0 }}\cdot t"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(equation_transposed, equation_integrated))
        self.wait(1)

        cleanup_text = mm.Text("整理...").move_to(mm.UP * 2)
        self.play(mm.ReplacementTransform(integrate_text, cleanup_text))
        self.wait(1)

        equation_expontiated = (
            mm.MathTex(
                R"{ 1 \over 1-{ [{{ P }}] \over {{ S_0 }} } }=\exp\left( {{ K }}{{ E_0 }}\cdot t \right)"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(equation_integrated, equation_expontiated))
        self.wait(1)

        equation_reciprocal = (
            mm.MathTex(
                R"1-{ [{{ P }}] \over {{ S_0 }} }=\exp\left( -{{ K }}{{ E_0 }}\cdot t \right)"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(equation_expontiated, equation_reciprocal))
        self.wait(1)

        equation_final = (
            mm.MathTex(
                R"[{{ P }}]=\left(1-\exp\left( -{{ K }}{{ E_0 }}\cdot t \right)\right){{ S_0 }}"
            )
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.ReplacementTransform(equation_reciprocal, equation_final))
        self.wait(1)

        model_derived_text = mm.Text("模型").move_to(mm.UP * 2)
        equation_model = (
            mm.MathTex(R"{{ y }}=(1-\exp( -{{ a }}{{ x }} )){{ b }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
        )
        self.play(
            mm.FadeOut(notation),
            mm.ReplacementTransform(cleanup_text, model_derived_text),
            mm.ReplacementTransform(equation_final, equation_model),
        )
        self.wait(1)

        N = 9
        arrow = mm.Arrow(mm.LEFT, mm.RIGHT)
        axes = mm.Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False},
        ).next_to(arrow, mm.RIGHT)
        x = np.linspace(0, 4, N)
        y = (1 - np.exp(-x / 2)) * 5 + np.random.normal(0, 0.25, N)
        points = mm.VGroup(
            *[mm.Dot(axes.c2p(x[i], y[i]), color=mm.RED) for i in range(len(x))]
        )
        fitted = axes.plot(lambda x: (1 - np.exp(-x / 2)) * 5)
        self.play(
            mm.FadeOut(model_derived_text),
            mm.Create(axes),
            mm.Create(points),
            equation_model.animate.scale(0.5).next_to(arrow, mm.LEFT),
        )
        self.play(mm.GrowArrow(arrow))
        self.play(mm.Create(fitted))
        self.wait(1)


class Fitting(mm.Scene):
    def construct(self):
        CMAP = {
            " E ": mm.RED,
            " E_0 ": mm.RED,
            " a ": mm.RED,
            " S ": mm.BLUE,
            " S_0 ": mm.BLUE,
            " b ": mm.BLUE,
            " ES ": mm.PURPLE,
            " P ": mm.GREEN,
        }
        N = 5
        FUNC = lambda x: (1 - np.exp(-x / 2)) * 5
        CODE_CONFIG = {
            "tab_width": 4,
            "background": "window",
            "insert_line_no": False,
            "style": "github-dark",
            "font": "XHei Intel Mono",
        }

        title = mm.Text("拟合", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        x = np.arange(N)
        y = FUNC(x) + np.random.normal(0, 0.15, N)
        table_hori = mm.DecimalTable(
            [x, y],
            row_labels=[
                mm.MathTex(R"t"),
                mm.MathTex(R"[{{ P }}]").set_color_by_tex_to_color_map(CMAP),
            ],
            element_to_mobject_config={"num_decimal_places": 3},
        )
        self.play(mm.Write(table_hori))
        self.wait(1)

        table_vert = mm.DecimalTable(
            [[x[i], y[i]] for i in range(N)],
            col_labels=[
                mm.MathTex(R"t"),
                mm.MathTex(R"[{{ P }}]").set_color_by_tex_to_color_map(CMAP),
            ],
            element_to_mobject_config={"num_decimal_places": 3},
        ).scale(0.75)
        self.play(mm.ReplacementTransform(table_hori, table_vert))
        self.wait(1)

        file_content = mm.Code(
            code="\n".join(["x,y"] + [f"{x[i]:.01f},{y[i]:.03f}" for i in range(N)]),
            language="text",
            **CODE_CONFIG | {"style": "default"},
        ).scale(1.5)
        self.play(mm.ReplacementTransform(table_vert, file_content))
        self.wait(1)

        file_object = (
            mm.VGroup(
                mm.RoundedRectangle(
                    height=3, width=4, color=mm.GREEN, fill_opacity=0.5
                ),
                mm.Text("data.csv"),
            )
            .scale(0.5)
            .to_corner(mm.DOWN + mm.LEFT)
        )
        self.play(mm.ReplacementTransform(file_content, file_object))
        self.wait(1)

        equation_model = (
            mm.MathTex(R"{{ y }}=(1-\exp( -{{ a }}{{ x }} )){{ b }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(2)
        )
        self.play(mm.Write(equation_model))
        self.wait(1)

        self.play(equation_model.animate.scale(0.5).to_edge(mm.RIGHT))
        self.play(mm.FadeOut(equation_model))
        self.wait(1)

        python_text = mm.Text("Python").move_to(mm.LEFT * 3)
        python_code = mm.Code(
            "./assets/fit.py", language="python", **CODE_CONFIG
        ).to_edge(mm.RIGHT)
        self.play(mm.Write(python_code))
        self.play(mm.Write(python_text))
        self.wait(1)

        self.play(mm.Circumscribe(python_code.code[5:8], color=mm.YELLOW))  # type: ignore
        self.wait(1)

        R_text = mm.Text("R").move_to(mm.LEFT * 3)
        R_code = mm.Code("./assets/fit.R", language="R", **CODE_CONFIG).to_edge(
            mm.RIGHT
        )
        self.play(
            mm.FadeTransformPieces(python_code, R_code),
            mm.ReplacementTransform(python_text, R_text),
        )
        self.wait(1)

        self.play(mm.Circumscribe(R_code.code[:4], color=mm.YELLOW))  # type: ignore
        self.wait(1)

        matlab_text = mm.Text("Matlab").move_to(mm.LEFT * 3)
        matlab_code = mm.Code(
            "./assets/fit.m", language="matlab", **CODE_CONFIG
        ).to_edge(mm.RIGHT)
        self.play(
            mm.FadeTransformPieces(R_code, matlab_code),
            mm.ReplacementTransform(R_text, matlab_text),
        )
        self.wait(1)

        self.play(mm.Circumscribe(matlab_code.code[:2], color=mm.YELLOW))  # type: ignore
        self.wait(1)

        equation_model.scale(2).center()
        self.play(mm.FadeOut(matlab_code, matlab_text, file_object))
        self.play(mm.Write(equation_model))
        self.wait(1)

        N = 10
        x = np.arange(N) / 2
        y = FUNC(x) + np.random.normal(0, 0.15, N)
        model = lambda x, a, b: (1 - np.exp(-a * x)) * b
        popt, pcov = curve_fit(model, x, y)
        fitted_a_label = (
            mm.MathTex(R"{{ a }}=").set_color_by_tex_to_color_map(CMAP).scale(2)
        )
        fitted_b_label = (
            mm.MathTex(R"{{ b }}=").set_color_by_tex_to_color_map(CMAP).scale(2)
        )
        value_a = mm.ValueTracker(1)
        value_b = mm.ValueTracker(5)
        value_a.set_value(popt[0])
        value_b.set_value(popt[1])
        value_a_text = (
            mm.DecimalNumber(number=value_a.get_value(), num_decimal_places=3)
            .scale(2)
            .next_to(fitted_a_label, mm.RIGHT)
        )
        value_a_text.add_updater(lambda v: v.set_value(value_a.get_value()))
        value_b_text = (
            mm.DecimalNumber(number=value_b.get_value(), num_decimal_places=3)
            .scale(2)
            .next_to(fitted_b_label, mm.RIGHT)
        )
        value_b_text.add_updater(lambda v: v.set_value(value_b.get_value()))
        equation_model.generate_target()
        mm.VGroup(
            equation_model.target,
            mm.VGroup(fitted_a_label, value_a_text),
            mm.VGroup(fitted_b_label, value_b_text),
        ).arrange(
            mm.DOWN  # type: ignore
        ).center()
        self.play(
            mm.MoveToTarget(equation_model),
            mm.LaggedStart(
                mm.Write(fitted_a_label),
                mm.Write(fitted_b_label),
                mm.Write(value_a_text),
                mm.Write(value_b_text),
            ),
        )
        self.wait(1)

        self.play(
            mm.VGroup(
                value_a_text,
                value_b_text,
                fitted_a_label,
                fitted_b_label,
                equation_model,
            )
            .animate.scale(0.75)
            .to_edge(mm.LEFT)
        )
        self.wait(1)

        axes = mm.Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": False},
        ).to_edge(mm.RIGHT)
        points = mm.VGroup(
            *[mm.Dot(axes.c2p(_x, _y), color=mm.RED) for _x, _y in zip(x, y)]
        )
        line_fitted = axes.plot(
            lambda x: (1 - np.exp(-value_a.get_value() * x)) * value_b.get_value(),
            color=mm.BLUE,
        )
        line_fitted.add_updater(
            lambda l: l.become(
                axes.plot(
                    lambda x: (1 - np.exp(-value_a.get_value() * x))
                    * value_b.get_value(),
                    color=mm.BLUE,
                )
            )  # type: ignore
        )
        self.play(mm.Write(axes))
        self.play(mm.Write(points))
        self.play(mm.Write(line_fitted))
        self.wait(1)

        line_actuale = mm.DashedVMobject(axes.plot(FUNC))
        self.play(mm.Write(line_actuale))
        self.wait(1)

        for _ in range(3):
            y = FUNC(x) + np.random.normal(0, 0.15, N)
            popt, pcov = curve_fit(model, x, y)
            self.play(
                points.animate.become(
                    mm.VGroup(
                        *[
                            mm.Dot(axes.c2p(_x, _y), color=mm.RED)
                            for _x, _y in zip(x, y)
                        ]
                    )
                )
            )
            self.play(
                value_a.animate.set_value(popt[0]), value_b.animate.set_value(popt[1])
            )
            self.wait(1)


class Next(mm.Scene):
    def construct(self):
        CMAP = {
            " S ": mm.YELLOW,
            " S' ": mm.BLUE,
            " a ": mm.RED,
            " KE_0 ": mm.RED,
            " E_0 ": mm.RED,
            " b ": mm.BLUE,
            " S_0 ": mm.BLUE,
        }
        N = 9
        FUNC = lambda x: (1 - np.exp(-x / 2)) * 5

        title = mm.Text("接下来", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        verfiy_text = mm.Text("验证模型").scale(1.5)
        self.play(mm.Write(verfiy_text))
        self.wait(1)

        R2 = mm.MathTex("R^2").scale(1.5).move_to(mm.LEFT * 3)
        axes = mm.Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": False},
        ).to_edge(mm.RIGHT)
        x = np.arange(N) / 2
        y = FUNC(x) + np.random.normal(0, 0.15, N)
        points = mm.VGroup(
            *[mm.Dot(axes.c2p(x[i], y[i]), color=mm.RED) for i in range(N)]
        )
        self.play(mm.ReplacementTransform(verfiy_text, R2))
        self.play(mm.Write(axes), mm.Write(points))
        self.wait(1)

        line_mean = axes.plot(lambda x: y.mean())
        self.play(mm.Write(line_mean))
        self.wait(1)

        error_mean = mm.VGroup(
            *[
                mm.Line(axes.c2p(x[i], y.mean()), axes.c2p(x[i], y[i]), color=mm.YELLOW)
                for i in range(N)
            ]
        )
        self.play(mm.Write(error_mean))
        self.wait(1)

        error_mean_squared = (
            mm.VGroup(
                *[
                    mm.Square(
                        side_length=np.abs(y[i] - y.mean()) / 2,
                        color=mm.YELLOW,
                        fill_opacity=0.5,
                    )
                    for i in range(N)
                ]
            )
            .arrange(buff=0.1)
            .next_to(R2, mm.DOWN, buff=0.5)
        )
        self.play(mm.ReplacementTransform(error_mean, error_mean_squared))
        self.wait(1)

        S_tot = (
            mm.MathTex("{{ S }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
            .next_to(R2, mm.DOWN, buff=0.5)
        )
        self.play(mm.ReplacementTransform(error_mean_squared, S_tot))
        self.wait(1)

        line_model = axes.plot(lambda x: FUNC(x))
        self.play(mm.ReplacementTransform(line_mean, line_model))
        self.wait(1)

        error_model = mm.VGroup(
            *[
                mm.Line(axes.c2p(x[i], FUNC(x[i])), axes.c2p(x[i], y[i]), color=mm.BLUE)
                for i in range(N)
            ]
        )
        self.play(mm.Write(error_model))
        self.wait(1)

        error_model_squared = (
            mm.VGroup(
                *[
                    mm.Square(
                        side_length=np.abs(y[i] - FUNC(x[i])) / 2,
                        color=mm.BLUE,
                        fill_opacity=0.5,
                    )
                    for i in range(N)
                ]
            )
            .arrange(buff=0.1)
            .next_to(R2, mm.UP, buff=0.5)
        )
        self.play(mm.ReplacementTransform(error_model, error_model_squared))
        self.wait(1)

        S_res = (
            mm.MathTex("{{ S' }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
            .next_to(R2, mm.UP, buff=0.5)
        )
        self.play(mm.ReplacementTransform(error_model_squared, S_res))
        self.wait(1)

        R2_formula = (
            mm.MathTex(R"{{ R^2 }}=1-{ {{ S' }} \over {{ S }} }")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
            .move_to(R2)
        )
        self.play(mm.ReplacementTransform(mm.VGroup(S_tot, S_res, R2), R2_formula))
        self.wait(1)

        self.play(mm.FadeOut(R2_formula, line_model, points, axes))
        self.wait(1)

        analysis_text = mm.Text("后续分析").scale(1.5)
        self.play(mm.Write(analysis_text))
        self.wait(1)

        model_formula = (
            mm.MathTex(R"{{ y }}=(1-\exp( -{{ a }}{{ x }} )){{ b }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.FadeTransform(analysis_text, model_formula))
        self.wait(1)

        model_formula.generate_target()
        original_formula = (
            mm.MathTex(R"[{{ P }}]=(1-\exp( -{{ KE_0 }}\cdot{{ t }} ))\cdot{{ S_0 }}")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
            .next_to(model_formula.target, mm.DOWN, buff=0.5)
        )
        mm.VGroup(original_formula, model_formula.target).center()
        self.play(mm.Write(original_formula), mm.MoveToTarget(model_formula))
        self.wait(1)

        K_tot = mm.MathTex(R"{{ KE_0 }}").set_color_by_tex_to_color_map(CMAP).scale(1.5)
        self.play(
            mm.FadeTransformPieces(original_formula, K_tot), mm.FadeOut(model_formula)
        )
        self.wait(1)

        K_avg = (
            mm.MathTex(R"{{ K }}={ {{ KE_0 }} \over {{ E_0 }} }")
            .set_color_by_tex_to_color_map(CMAP)
            .scale(1.5)
        )
        self.play(mm.FadeTransformPieces(K_tot, K_avg))
        self.wait(1)

        # copy and distribute 10 of K_avg
        Ks = mm.VGroup(*[K_avg[0].copy() for _ in range(10)])
        for i in range(10):
            Ks[i].generate_target()
            Ks[i].target.set_color(mm.YELLOW).scale(np.random.normal(1, 0.25))  # type: ignore
        mm.VGroup(*[K.target for K in Ks]).arrange(buff=0.5).next_to(
            K_avg, mm.DOWN, buff=1
        )
        self.play(
            mm.LaggedStart(*[mm.MoveToTarget(K) for K in Ks], lag_ratio=0.1, run_time=2)
        )
        self.wait(1)

        Kss = (
            mm.VGroup(
                *[
                    mm.MathTex(R"{{ K' }}")
                    .set_color(mm.BLUE)  # type: ignore
                    .scale(np.random.normal(1, 0.25))
                    for _ in range(10)
                ]
            )
            .arrange(buff=0.5)
            .next_to(K_avg, mm.UP, buff=1)
        )
        self.play(mm.ReplacementTransform(Ks.copy(), Kss))
        self.wait(1)

        hypothesis_testing_text = mm.Text("假设检验").scale(1.5)
        self.play(mm.ReplacementTransform(K_avg, hypothesis_testing_text))
        self.wait(1)


class Conclusion(mm.Scene):
    def construct(self):
        title = mm.Text("总结", color=mm.BLUE).scale(2)
        self.play(mm.Write(title))
        self.wait(1)
        self.play(
            title.animate.scale(0.5).set_color(mm.WHITE).to_corner(mm.UP + mm.LEFT)
        )

        modelling_text = mm.Text("建模").scale(1.5)
        self.play(mm.Write(modelling_text))
        self.wait(1)
        self.play(modelling_text.animate.to_edge(mm.LEFT, buff=1))
        self.wait(1)

        forward_text = mm.Text("正向建模")
        backward_text = mm.Text("反向建模")
        (
            mm.VGroup(backward_text, forward_text)
            .arrange(mm.DOWN, buff=0.75)  # type: ignore
            .next_to(modelling_text, mm.RIGHT, buff=1)
        )
        brace_1 = mm.Brace(mm.VGroup(backward_text, forward_text), mm.LEFT)  # type: ignore
        self.play(mm.GrowFromCenter(brace_1))
        self.play(mm.Write(backward_text))
        self.play(mm.Write(forward_text))
        self.wait(1)

        backward_text.generate_target()
        forward_text.generate_target()
        deep_learning_text = mm.Text("深度学习").next_to(backward_text, mm.UP, buff=0.75)
        mm.VGroup(
            backward_text.target,
            forward_text.target,
            deep_learning_text,
        ).next_to(modelling_text, mm.RIGHT, buff=1)
        brace_2 = mm.Brace(
            mm.VGroup(deep_learning_text, backward_text.target, forward_text.target), mm.LEFT  # type: ignore
        )
        self.play(
            mm.Write(deep_learning_text),
            mm.MoveToTarget(backward_text),
            mm.MoveToTarget(forward_text),
            mm.ReplacementTransform(brace_1, brace_2),
        )
        self.wait(1)

        input_layer = mm.VGroup(
            *[mm.Circle(radius=0.15, color=mm.BLUE) for _ in range(5)]
        ).arrange(
            mm.DOWN, buff=0.5  # type: ignore
        )
        hidden_layer = mm.VGroup(
            *[mm.Circle(radius=0.15, color=mm.GREEN) for _ in range(3)]
        ).arrange(
            mm.DOWN, buff=0.5  # type: ignore
        )
        output_layer = mm.VGroup(
            *[mm.Circle(radius=0.15, color=mm.RED) for _ in range(4)]
        ).arrange(
            mm.DOWN, buff=0.5  # type: ignore
        )
        input_label = mm.MathTex(R"{{ x }}", color=mm.BLUE).scale(2)
        output_label = mm.MathTex(R"{{ y }}", color=mm.RED).scale(2)
        (
            mm.VGroup(
                input_label, input_layer, hidden_layer, output_layer, output_label
            )
            .arrange(mm.RIGHT, buff=1)  # type: ignore
            .to_edge(mm.RIGHT)
        )
        i2h = mm.VGroup(
            *[
                mm.Line(i.get_right(), h.get_left())
                for i in input_layer
                for h in hidden_layer
            ]
        )
        h2o = mm.VGroup(
            *[
                mm.Line(h.get_right(), o.get_left())
                for h in hidden_layer
                for o in output_layer
            ]
        )
        self.play(mm.Write(input_label))
        self.play(mm.Write(output_label))
        self.play(
            mm.LaggedStart(
                *[
                    mm.LaggedStart(
                        *[mm.Create(n) for n in layer],
                        lag_ratio=0.1,
                        run_time=2,
                    )
                    for layer in [input_layer, hidden_layer, output_layer]
                ],
                lag_ratio=0.1,
            )
        )
        self.play(
            mm.LaggedStart(
                *[
                    mm.LaggedStart(
                        *[mm.Write(n) for n in layer],
                        lag_ratio=0.1,
                        run_time=2,
                    )
                    for layer in [i2h, h2o]
                ],
                lag_ratio=0.1,
            )
        )
        self.wait(1)

        self.play(
            mm.FadeOut(
                i2h,
                h2o,
                input_label,
                output_label,
                input_layer,
                hidden_layer,
                output_layer,
            )
        )
        self.wait(1)

        deep_learning_text.generate_target()
        gaussian_process_text = mm.Text("高斯过程").next_to(
            deep_learning_text, mm.UP, buff=0.75
        )
        mm.VGroup(
            backward_text.target,
            forward_text.target,
            deep_learning_text.target,
            gaussian_process_text,
        ).next_to(modelling_text, mm.RIGHT, buff=1)
        brace_3 = mm.Brace(
            mm.VGroup(
                gaussian_process_text,
                deep_learning_text.target,
                backward_text.target,
                forward_text.target,
            ),
            mm.LEFT,  # type: ignore
        )
        self.play(
            mm.Write(gaussian_process_text),
            mm.MoveToTarget(deep_learning_text),
            mm.MoveToTarget(backward_text),
            mm.MoveToTarget(forward_text),
            mm.ReplacementTransform(brace_2, brace_3),
        )
        self.wait(1)

        axes = mm.Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": False},
        ).to_edge(mm.RIGHT)
        self.play(mm.Create(axes))
        self.wait(1)

        kernel = 1 * RBF() + 0
        gpr = GPR(kernel)
        x = np.array([-2, 1, 0])
        y = np.array([1, -1, 0])
        line_0 = axes.plot(
            lambda x: gpr.predict(np.array([x]).reshape(-1, 1)).squeeze()  # type: ignore
        )
        self.play(mm.Create(line_0))
        self.wait(1)

        point_1 = mm.Dot(axes.c2p(x[0], y[0]), color=mm.RED)
        gpr.fit(x[:1].reshape(-1, 1), y[:1].reshape(-1, 1))
        line_1 = axes.plot(
            lambda x: gpr.predict(np.array([x]).reshape(-1, 1)).squeeze()  # type: ignore
        )
        self.play(mm.Create(point_1), mm.ReplacementTransform(line_0, line_1))
        self.wait(1)

        point_2 = mm.Dot(axes.c2p(x[1], y[1]), color=mm.RED)
        gpr.fit(x[:2].reshape(-1, 1), y[:2].reshape(-1, 1))
        line_2 = axes.plot(
            lambda x: gpr.predict(np.array([x]).reshape(-1, 1)).squeeze()  # type: ignore
        )
        self.play(mm.Create(point_2), mm.ReplacementTransform(line_1, line_2))
        self.wait(1)

        point_3 = mm.Dot(axes.c2p(x[2], y[2]), color=mm.RED)
        gpr.fit(x[:3].reshape(-1, 1), y[:3].reshape(-1, 1))
        line_3 = axes.plot(
            lambda x: gpr.predict(np.array([x]).reshape(-1, 1)).squeeze()  # type: ignore
        )
        self.play(mm.Create(point_3), mm.ReplacementTransform(line_2, line_3))
        self.wait(1)

        gaussian_process_text.generate_target()
        more_text = mm.Text("...").next_to(forward_text, mm.DOWN, buff=0.75)
        mm.VGroup(
            gaussian_process_text.target,
            deep_learning_text.target,
            backward_text.target,
            forward_text.target,
            more_text,
        ).next_to(modelling_text, mm.RIGHT, buff=1)
        brace_4 = mm.Brace(
            mm.VGroup(
                backward_text.target,
                forward_text.target,
                deep_learning_text.target,
                gaussian_process_text.target,
                more_text,
            ),
            mm.LEFT,  # type: ignore
        )
        self.play(
            mm.Write(more_text),
            mm.MoveToTarget(gaussian_process_text),
            mm.MoveToTarget(deep_learning_text),
            mm.MoveToTarget(backward_text),
            mm.MoveToTarget(forward_text),
            mm.ReplacementTransform(brace_3, brace_4),
        )
        self.wait(1)

        self.play(
            mm.FadeOut(
                brace_4,
                gaussian_process_text,
                deep_learning_text,
                backward_text,
                forward_text,
                more_text,
                point_1,
                point_2,
                point_3,
                line_3,
                axes,
            ),
            modelling_text.animate.center(),
        )
        self.wait(1)

        thanks_text = mm.Text("感谢观看").scale(2)
        self.play(
            mm.ReplacementTransform(modelling_text, thanks_text), mm.FadeOut(title)
        )
        self.wait(1)

        thanks_text.generate_target()
        wish_text = mm.Text("祝大家学习顺利")
        mm.VGroup(thanks_text.target, wish_text).arrange(mm.DOWN, buff=0.75)  # type: ignore
        self.play(mm.MoveToTarget(thanks_text), mm.Write(wish_text))
        self.wait(1)

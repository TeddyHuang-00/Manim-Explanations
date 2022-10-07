from manim import *
import numpy as np

np.random.seed(0)


class Opening(Scene):
    def construct(self):
        t_title = Text("理解计算机程序").scale(2)
        t_chap1 = Text("什么是程序")
        t_chap2 = Text("程序如何运行")
        t_chap3 = Text("如何写好程序")

        self.play(Write(t_title))
        self.wait(2)
        self.play(Transform(t_title, t_chap1))
        self.wait(2)
        self.play(Transform(t_title, t_chap2))
        self.wait(2)
        self.play(Transform(t_title, t_chap3))
        self.wait(2)
        self.play(FadeOut(t_title))
        self.wait(2)


class SourceFile(Scene):
    def construct(self):
        # print(Code.styles_list)
        cpp_file_title = Text("C++")
        c_file_title = Text("C")
        cpp_file_content = Code(
            "hello_world.cpp",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        c_file_content = Code(
            "hello_world.c",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        cpp_file_content.next_to(cpp_file_title, DOWN)
        VGroup(cpp_file_title, cpp_file_content)
        c_file_content.next_to(c_file_title, DOWN)
        VGroup(c_file_title, c_file_content).next_to(
            VGroup(cpp_file_title, cpp_file_content), LEFT
        )
        c_file_title.align_to(cpp_file_title, UP)
        c_file_content.align_to(cpp_file_content, UP)

        t_title = Text("源文件")
        t_title.generate_target()
        t_title.target.set_fill(color=BLUE)
        t_title.target.to_edge(UL)
        t_title.target.scale(0.75)
        t_head = (
            Text("头文件", color=RED)
            .scale(0.5)
            .set_y(
                (cpp_file_content.code[0].get_y() + c_file_content.code[0].get_y()) / 2
            )
        )
        t_output = (
            Text("输出语句", color=YELLOW)
            .scale(0.5)
            .set_y(
                (cpp_file_content.code[4].get_y() + c_file_content.code[4].get_y()) / 2
            )
        )

        VGroup(cpp_file_title, cpp_file_content).next_to(
            VGroup(t_head, t_output), RIGHT
        )
        VGroup(c_file_title, c_file_content).next_to(VGroup(t_head, t_output), LEFT)
        VGroup(
            cpp_file_title,
            cpp_file_content,
            c_file_title,
            c_file_content,
            t_output,
            t_head,
        ).center()

        # self.add(NumberPlane())
        self.play(Write(t_title))
        self.wait(2)
        self.play(MoveToTarget(t_title))
        self.play(Write(cpp_file_title), Write(c_file_title))
        self.play(Write(cpp_file_content), Write(c_file_content))
        self.wait(2)
        self.play(
            Circumscribe(c_file_content.code[0], color=RED),
            Circumscribe(cpp_file_content.code[0], color=RED),
            Write(t_head),
            runtime=2,
        )
        self.wait(2)
        self.play(
            Circumscribe(c_file_content.code[4], color=YELLOW),
            Circumscribe(cpp_file_content.code[4], color=YELLOW),
            Write(t_output),
            runtime=2,
        )
        self.wait(2)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait(2)


class Compile(Scene):
    def construct(self):
        position_list = [
            [-1, 1.5, 0],
            [-1, -1.5, 0],
            [1, -1, 0],
            [1, 1, 0],
        ]
        g_compiler = (
            Polygon(*position_list, color=PURPLE)
            .set_fill(PURPLE, 0.5)
            .round_corners(0.25)
        )

        t_title = Text("编译")
        t_title.generate_target()
        t_title.target.set_fill(BLUE)
        t_title.target.to_edge(UL)
        t_title.target.scale(0.75)

        t_source = Text("源文件").to_edge(LEFT).shift(RIGHT)
        t_source.generate_target()
        t_source.target.set_fill(PURPLE).center().scale(0.0)
        t_target = Text("可执行程序").to_edge(RIGHT).shift(LEFT)
        t_target.generate_target()
        t_target.set_fill(PURPLE).center().scale(0.0)
        t_compiler = Text("编译器").move_to(g_compiler.center())

        e_source = Text("hello.c/.cpp").to_edge(LEFT).scale(0.75)
        e_target = Text("hello.out/.exe").to_edge(RIGHT).scale(0.75)
        e_compiler = (
            Paragraph("gcc", "g++", "clang", "clang++", alignment="center")
            .move_to(g_compiler.center())
            .scale(0.75)
        )

        # self.add(NumberPlane())
        self.play(Write(t_title))
        self.wait(2)
        self.play(MoveToTarget(t_title))
        self.play(
            DrawBorderThenFill(g_compiler),
            LaggedStart(Write(t_compiler), lag_ratio=0.5),
        )
        self.wait(2)
        self.play(FadeIn(t_source))
        self.wait(2)
        self.play(MoveToTarget(t_source))
        self.remove(t_source)
        self.add(t_target)
        self.play(MoveToTarget(t_target))
        self.wait(2)
        self.play(
            FadeIn(e_source),
            Transform(t_target, e_target),
            Transform(t_compiler, e_compiler),
        )
        self.wait(2)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait(2)


class CompileDetails(Scene):
    def construct(self):
        t_title = Text("编译过程")

        ch_1_title = Text("预处理")
        ch_1_title.generate_target()
        ch_1_title.target.set_fill(BLUE)
        ch_1_title.target.to_edge(UL)
        ch_1_title.target.scale(0.75)

        ch_2_title = Text("编译")
        ch_2_title.generate_target()
        ch_2_title.target.set_fill(BLUE)
        ch_2_title.target.to_edge(UL)
        ch_2_title.target.scale(0.75)

        ch_3_title = Text("汇编与连接")
        ch_3_title.generate_target()
        ch_3_title.target.set_fill(BLUE)
        ch_3_title.target.to_edge(UL)
        ch_3_title.target.scale(0.75)

        code_source = Code(
            "hello_world.c",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        code_processed = Code(
            "hello_world.i",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        code_compiled = Code(
            "hello_world.s",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        code_assembled = Paragraph(
            *[
                "".join(map(str, line))
                for line in np.random.randint(0, 2, 32).reshape(-1, 8).tolist()
            ],
            "0_printf",
            *[
                "".join(map(str, line))
                for line in np.random.randint(0, 2, 24).reshape(-1, 8).tolist()
            ],
            alignment="center",
            color=YELLOW,
            font="XHei NF",
        ).scale(0.5)
        code_printf = Paragraph(
            *[
                "".join(map(str, line))
                for line in np.random.randint(0, 2, 36).reshape(6, -1).tolist()
            ],
            alignment="center",
            color=BLUE,
            font="XHei NF",
        ).scale(0.5)
        code_executable = Paragraph(
            *[
                "".join(map(str, line))
                for line in np.random.randint(0, 2, 96).reshape(8, -1).tolist()
            ],
            alignment="center",
            color=GREEN,
            font="XHei NF",
        ).scale(0.5)

        t_source = Text("源文件").next_to(code_source, UP)
        VGroup(t_source, code_source).center()
        t_preprocessed = Text("预处理后").next_to(code_processed, UP)
        VGroup(t_preprocessed, code_processed).center()
        t_head = Text("stdio.h", color=GREEN).to_edge(RIGHT).shift(LEFT * 0.5)
        t_compiled = Text("汇编程序").next_to(code_compiled, UP)
        VGroup(t_compiled, code_compiled).center()
        t_assembled = Text("目标文件").next_to(code_assembled, UP)
        VGroup(t_assembled, code_assembled).center()
        t_printf = Text("printf.o").next_to(code_printf, UP)
        VGroup(t_printf, code_printf).to_edge(RIGHT)
        t_executable = Text("完整程序").next_to(code_executable, UP)
        VGroup(t_executable, code_executable).center()

        a_preprocess = Arrow(
            start=code_source.code[0].get_right(), end=t_head.get_left(), color=GREEN
        )

        # self.add(NumberPlane())
        self.play(Write(t_title))
        self.wait(2)

        # Preprocess
        self.play(Transform(t_title, ch_1_title))
        self.wait(2)
        self.remove(t_title)
        self.play(MoveToTarget(ch_1_title))
        self.play(Write(t_source), Write(code_source))
        self.wait(2)
        self.play(Write(t_head), LaggedStart(GrowArrow(a_preprocess)))
        self.wait(2)
        self.play(
            Transform(code_source, code_processed),
            Transform(t_source, t_preprocessed),
            FadeOut(t_head),
            FadeOut(a_preprocess),
        )
        self.wait(2)

        # Compile
        self.remove(t_source, code_source)
        self.play(
            Transform(ch_1_title, ch_2_title),
            VGroup(t_preprocessed, code_processed).animate.shift(DOWN * 2).scale(0.25),
        )
        self.wait(2)
        self.remove(ch_1_title)
        self.play(
            MoveToTarget(ch_2_title),
            VGroup(t_preprocessed, code_processed).animate.shift(UP * 2).scale(4.0),
        )
        self.wait(2)
        self.play(
            FocusOn(code_processed, run_time=1),
            Transform(code_processed, code_compiled),
            Transform(t_preprocessed, t_compiled),
        )
        self.wait(2)

        # Assembly & Link
        self.remove(t_preprocessed, code_processed)
        self.play(
            Transform(ch_2_title, ch_3_title),
            VGroup(t_compiled, code_compiled).animate.shift(DOWN * 2).scale(0.25),
        )
        self.wait(2)
        self.remove(ch_2_title)
        self.play(
            MoveToTarget(ch_3_title),
            VGroup(t_compiled, code_compiled).animate.shift(UP * 2).scale(4.0),
        )
        self.wait(2)
        self.play(
            FocusOn(code_compiled, run_time=1),
            Transform(code_compiled, code_assembled),
            Transform(t_compiled, t_assembled),
        )
        self.wait(2)
        self.remove(t_compiled, code_compiled)
        self.add(t_assembled, code_assembled)
        a_link = Arrow(
            start=code_assembled[4].get_right(),
            end=code_printf.get_left(),
            color=BLUE,
        )
        self.play(Write(t_printf), Write(code_printf), LaggedStart(GrowArrow(a_link)))
        self.wait(2)
        self.play(
            Transform(VGroup(code_assembled, code_printf), code_executable),
            Transform(VGroup(t_assembled, t_printf), t_executable),
            FadeOut(a_link),
        )
        self.wait(2)

        # Clear
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )
        self.wait(2)


class Execute(Scene):
    def construct(self):
        t_title = Text("运行")
        t_title.generate_target()
        t_title.target.set_fill(BLUE)
        t_title.target.to_edge(UL)
        t_title.target.scale(0.75)

        position_list = [
            [-1, 1.5, 0],
            [-1, -1.5, 0],
            [1, -1, 0],
            [1, 1, 0],
        ]
        g_program = (
            Polygon(*position_list, color=GREEN)
            .set_fill(GREEN, 0.5)
            .round_corners(0.25)
        )
        g_program.generate_target()
        t_program = Text("程序").move_to(g_program.center())
        t_program.generate_target()

        g_memory = (
            Table(
                [["0x0000", "..."], ["", "..."]],
                row_labels=[Text("地址"), Text("内容")],
                include_outer_lines=True,
                include_background_rectangle=True,
            )
            .scale(0.5)
            .next_to(g_program, DOWN, buff=1.5)
        )
        t_memory = Text("内存").scale(0.75).next_to(g_memory, LEFT)
        t_input = Text("输入").scale(0.75).to_edge(LEFT).shift(RIGHT)
        t_input.generate_target()
        t_output = Text("输出").scale(0.75).to_edge(RIGHT).shift(LEFT)
        t_output.generate_target()
        a_input = Arrow(start=t_input.get_right(), end=g_program.get_left())
        a_input.generate_target()
        a_output = Arrow(start=g_program.get_right(), end=t_output.get_left())
        a_output.generate_target()
        a_m2p = Arrow(start=g_memory.get_top(), end=g_program.get_bottom()).shift(
            LEFT * 0.25
        )
        a_p2m = Arrow(start=g_program.get_bottom(), end=g_memory.get_top()).shift(
            RIGHT * 0.25
        )
        VGroup(
            t_input.target,
            a_input.target,
            t_output.target,
            a_output.target,
            t_program.target,
            g_program.target,
            t_memory,
            g_memory,
            a_p2m,
            a_m2p,
        ).center()

        e_program = Text("hello\n程序").move_to(t_program.target)
        e_input = MathTex(r"\emptyset").scale(1.5).move_to(t_input.target)
        e_output = Text("Hello world!").scale(0.75).move_to(t_output.target)
        a_e_input = Arrow(start=e_input.get_right(), end=g_program.target.get_left())
        a_e_output = Arrow(start=g_program.target.get_right(), end=e_output.get_left())
        t_string = Text("Hello world!").scale(0.4).move_to(g_memory.get_cell((2, 2)))

        self.play(Write(t_title))
        self.wait(2)
        self.play(MoveToTarget(t_title))
        self.play(Write(g_program), Write(t_program))
        self.wait(2)
        self.play(Write(t_input), GrowArrow(a_input))
        self.wait(2)
        self.play(Write(t_output), GrowArrow(a_output))
        self.wait(2)
        self.play(
            MoveToTarget(t_input),
            MoveToTarget(a_input),
            MoveToTarget(t_output),
            MoveToTarget(a_output),
            MoveToTarget(t_program),
            MoveToTarget(g_program),
        )
        self.play(Write(t_memory), Write(g_memory), GrowArrow(a_m2p), GrowArrow(a_p2m))
        self.wait(2)
        self.play(Transform(t_program, e_program), Write(t_string))
        self.play(Indicate(t_string))
        self.wait(2)
        self.play(Transform(t_input, e_input), Transform(a_input, a_e_input))
        self.remove(t_input)
        self.play(Indicate(e_input))
        self.remove(a_input)
        self.play(ApplyWave(a_e_input))
        self.wait(1)
        self.play(Indicate(g_program))
        self.wait(1)
        self.play(Indicate(t_string))
        self.play(ApplyWave(a_m2p, LEFT))
        self.wait(1)
        self.play(Transform(a_output, a_e_output), Transform(t_output, e_output))
        self.remove(a_output)
        self.play(ApplyWave(a_e_output))
        self.remove(t_output)
        self.play(Indicate(e_output))
        self.wait(2)


class APlusB(Scene):
    def construct(self):
        t_title = Text("一般程序")
        t_title.generate_target()
        t_title.target.set_fill(BLUE)
        t_title.target.to_edge(UL)
        t_title.target.scale(0.75)

        code_ff = Code(
            "APlusBFF.c",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        code_f = Code(
            "APlusBF.c",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        code_t = Code(
            "APlusB.c",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        t_source = Text("A+B?").next_to(code_ff, UP)
        VGroup(t_source, code_ff).center()

        position_list = [
            [-1, 1.5, 0],
            [-1, -1.5, 0],
            [1, -1, 0],
            [1, 1, 0],
        ]
        g_program = (
            Polygon(*position_list, color=GREEN)
            .set_fill(GREEN, 0.5)
            .round_corners(0.25)
            .rotate(-0.5 * PI)
        )
        t_program = Text("可执行程序").scale(0.75).move_to(g_program)
        VGroup(g_program, t_program).center()

        g_memory = (
            Table(
                [["&a", ""], ["&b", ""], ["&sum", ""]],
                col_labels=[Text("地址"), Text("内容")],
            )
            .scale(0.6)
            .to_edge(RIGHT)
            .shift(LEFT)
        )
        v_a = VMobject().move_to(g_memory.get_cell((2, 2)))
        v_b = VMobject().move_to(g_memory.get_cell((3, 2)))
        v_sum = VMobject().move_to(g_memory.get_cell((4, 2)))
        v_output = VMobject().to_edge(DOWN).shift(0.5 * UP)
        v_input = Text("3 4").to_edge(UP).shift(0.5 * DOWN)
        a_input = Arrow(start=v_input.get_bottom(), end=g_program.get_top())
        v_question = VMobject()

        g_breakpoint = Dot(color=RED).to_edge(LEFT).shift(0.5 * RIGHT)

        self.play(Write(t_title))
        self.wait(2)
        self.play(MoveToTarget(t_title))
        self.wait(2)
        # Faulty code 1
        self.play(Write(code_ff), Write(t_source))
        self.wait(2)
        self.play(
            VGroup(t_source, code_ff).animate.scale(0.75).to_edge(LEFT).shift(RIGHT)
        )
        self.wait(2)
        self.play(Write(g_program), Write(t_program))
        self.play(
            FadeIn(g_breakpoint),
            LaggedStart(g_breakpoint.animate.align_to(code_ff.code[2], DOWN)),
        )
        self.play(Circumscribe(code_ff.code[2], color=RED), Indicate(g_program))
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_ff.code[4], DOWN))
        self.play(
            Circumscribe(code_ff.code[4], color=RED), LaggedStart(Write(g_memory))
        )
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_ff.code[5], DOWN))
        self.play(Circumscribe(code_ff.code[5], color=RED))
        self.add(v_a, v_b, v_sum, v_output)
        self.play(Transform(v_a, Tex(r"1").move_to(g_memory.get_cell((2, 2)))))
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_ff.code[6], DOWN))
        self.play(Circumscribe(code_ff.code[6], color=RED))
        self.play(Transform(v_b, Tex(r"2").move_to(g_memory.get_cell((3, 2)))))
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_ff.code[7], DOWN))
        self.play(Circumscribe(code_ff.code[7], color=RED))
        self.play(Transform(v_sum, Tex(r"3").move_to(g_memory.get_cell((4, 2)))))
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_ff.code[8], DOWN))
        self.play(Circumscribe(code_ff.code[8], color=RED))
        self.play(v_sum.copy().animate.center().scale(0.0))
        self.play(Transform(v_output, Tex(r"3").to_edge(DOWN).shift(0.5 * UP)))
        a_output = Arrow(start=g_program.get_bottom(), end=v_output.get_top())
        self.play(GrowArrow(a_output))
        self.wait(2)
        self.play(Write(v_input), GrowArrow(a_input))
        self.play(
            Transform(
                v_question,
                Text("?", color=RED).scale(2.0).move_to(a_input.get_center()),
            ),
            Wiggle(a_input),
        )
        self.wait(2)
        # Faulty code 2
        self.play(
            FadeOut(v_question),
            FadeOut(v_input),
            FadeOut(a_input),
            FadeOut(v_output),
            FadeOut(a_output),
            FadeOut(v_a),
            FadeOut(v_b),
            FadeOut(v_sum),
        )
        v_question.become(VMobject())
        v_input.become(VMobject())
        v_output.become(VMobject())
        v_a.become(VMobject())
        v_b.become(VMobject())
        v_sum.become(VMobject())
        code_f.scale(0.75).move_to(code_ff).align_to(code_ff, UP)
        self.play(
            Transform(code_ff, code_f),
            Transform(t_source, Text("A+B??").scale(0.75).next_to(code_f, UP)),
            g_breakpoint.animate.align_to(code_ff.code[4], DOWN),
        )
        self.add(code_f)
        self.remove(code_ff)
        self.wait(2)
        self.play(g_breakpoint.animate.align_to(code_f.code[5], DOWN))
        self.play(Circumscribe(code_f.code[5], color=RED))
        v_input.become(Text("3 4").to_edge(UP).shift(0.5 * DOWN))
        self.play(Write(v_input), GrowArrow(a_input))
        self.add(v_a, v_b, v_sum, v_output)
        self.play(
            Transform(v_a, Tex(r"3").move_to(g_memory.get_cell((2, 2)))),
            Transform(v_b, Tex(r"4").move_to(g_memory.get_cell((3, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_f.code[6], DOWN),
            Circumscribe(code_f.code[6], color=RED),
            Transform(v_a, Tex(r"1").move_to(g_memory.get_cell((2, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_f.code[7], DOWN),
            Circumscribe(code_f.code[7], color=RED),
            Transform(v_b, Tex(r"2").move_to(g_memory.get_cell((3, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_f.code[8], DOWN),
            Circumscribe(code_f.code[8], color=RED),
            Transform(v_sum, Tex(r"3").move_to(g_memory.get_cell((4, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_f.code[9], DOWN),
            Circumscribe(code_f.code[9], color=RED),
            v_sum.copy().animate.center().scale(0.0),
            Transform(v_output, Tex(r"3").to_edge(DOWN).shift(0.5 * UP)),
            LaggedStart(GrowArrow(a_output)),
        )
        self.wait(2)
        self.play(
            Transform(
                v_question,
                Text("?", color=RED).scale(2.0).move_to(a_output.get_center()),
            ),
            Wiggle(a_output),
        )
        self.wait(2)
        # Correct code
        self.play(
            FadeOut(v_question),
            FadeOut(v_input),
            FadeOut(a_input),
            FadeOut(v_output),
            FadeOut(a_output),
            FadeOut(v_a),
            FadeOut(v_b),
            FadeOut(v_sum),
        )
        v_question.become(VMobject())
        v_input.become(VMobject())
        v_output.become(VMobject())
        v_a.become(VMobject())
        v_b.become(VMobject())
        v_sum.become(VMobject())
        code_t.scale(0.75).move_to(code_f).align_to(code_ff, UP)
        self.play(
            Transform(code_f, code_t),
            Transform(t_source, Text("A+B").scale(0.75).next_to(code_f, UP)),
            g_breakpoint.animate.align_to(code_f.code[4], DOWN),
        )
        self.add(code_t)
        self.remove(code_f)
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_t.code[5], DOWN),
            Circumscribe(code_t.code[5], color=RED),
        )
        v_input.become(Text("3 4").to_edge(UP).shift(0.5 * DOWN))
        self.play(Write(v_input), GrowArrow(a_input))
        self.add(v_a, v_b, v_sum, v_output)
        self.play(
            Transform(v_a, Tex(r"3").move_to(g_memory.get_cell((2, 2)))),
            Transform(v_b, Tex(r"4").move_to(g_memory.get_cell((3, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_t.code[6], DOWN),
            Circumscribe(code_t.code[6], color=RED),
            Transform(v_sum, Tex(r"7").move_to(g_memory.get_cell((4, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_t.code[7], DOWN),
            Circumscribe(code_t.code[7], color=RED),
            v_sum.copy().animate.center().scale(0.0),
            Transform(v_output, Tex(r"7").to_edge(DOWN).shift(0.5 * UP)),
            LaggedStart(GrowArrow(a_output)),
        )
        self.wait(2)
        self.play(
            FadeOut(a_output),
            Transform(v_output, VMobject()),
            Transform(v_input, Text("5 6").to_edge(UP).shift(0.5 * DOWN)),
        )
        self.play(
            g_breakpoint.animate.align_to(code_t.code[5], DOWN),
            Circumscribe(code_t.code[5], color=RED),
        )
        self.play(
            Transform(v_a, Tex(r"5").move_to(g_memory.get_cell((2, 2)))),
            Transform(v_b, Tex(r"6").move_to(g_memory.get_cell((3, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_t.code[6], DOWN),
            Circumscribe(code_t.code[6], color=RED),
            Transform(v_sum, Tex(r"11").move_to(g_memory.get_cell((4, 2)))),
        )
        self.wait(2)
        self.play(
            g_breakpoint.animate.align_to(code_t.code[7], DOWN),
            Circumscribe(code_t.code[7], color=RED),
            v_sum.copy().animate.center().scale(0.0),
            Transform(v_output, Tex(r"11").to_edge(DOWN).shift(0.5 * UP)),
            LaggedStart(GrowArrow(a_output)),
        )
        self.wait(2)
        self.play(
            FadeOut(g_breakpoint),
            Transform(v_input, Text("3 7").to_edge(UP).shift(0.5 * DOWN)),
        )
        self.wait(1)
        self.play(
            Circumscribe(code_t.code[5], color=RED),
            Transform(v_a, Tex(r"3").move_to(g_memory.get_cell((2, 2)))),
            Transform(v_b, Tex(r"7").move_to(g_memory.get_cell((3, 2)))),
        )
        self.wait(1)
        self.play(
            Circumscribe(code_t.code[6], color=RED),
            Transform(v_sum, Tex(r"10").move_to(g_memory.get_cell((4, 2)))),
        )
        self.wait(1)
        self.play(
            Circumscribe(code_t.code[7], color=RED),
            Transform(v_output, Tex(r"10").to_edge(DOWN).shift(0.5 * UP)),
        )
        self.wait(1)
        self.play(Transform(v_input, Text("2 5").to_edge(UP).shift(0.5 * DOWN)))
        self.play(
            Transform(v_a, Tex(r"2").move_to(g_memory.get_cell((2, 2)))),
            Transform(v_b, Tex(r"5").move_to(g_memory.get_cell((3, 2)))),
        )
        self.play(Transform(v_sum, Tex(r"7").move_to(g_memory.get_cell((4, 2)))))
        self.play(Transform(v_output, Tex(r"7").to_edge(DOWN).shift(0.5 * UP)))
        self.wait(2)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait(2)


class Conclusion(Scene):
    def construct(self):
        t_title = Text("总结")
        t_what = Text("什么是程序")
        t_how = Text("如何写好程序")

        l_1 = Text(
            "程序是一系列计算机指令（机器语言）的合集，能够实现特定功能或运算。",
            t2c={"输入": RED, "输出": BLUE, "运算": PURPLE},
        ).scale(0.5)
        l_2 = (
            Text(
                "C/C++ 等高级语言（可能经由汇编语言）最终将转化为机器语言供计算机执行。",
                t2c={"输入": RED, "输出": BLUE, "运算": PURPLE},
            )
            .scale(0.5)
            .next_to(l_1, DOWN, buff=1.5)
            .align_to(l_1, LEFT)
        )
        l_3 = (
            Text(
                "典型的程序能够处理固定格式的输入，并且将运算后得到的结果输出。",
                t2c={"输入": RED, "输出": BLUE, "运算": PURPLE},
            )
            .scale(0.5)
            .next_to(l_2, DOWN, buff=1.5)
            .align_to(l_2, LEFT)
        )
        VGroup(l_1, l_2, l_3).center()

        code_source = Code(
            "GoodExample.cpp",
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="XHei NF",
        )
        t_source = Text("良好的程序").next_to(code_source, UP)
        VGroup(t_source, code_source).center().to_edge(RIGHT).shift(0.5 * LEFT).scale(
            0.75
        )

        p_list = (
            Paragraph(
                "合适的头文件：使用已定义的函数",
                "变量：存放数据",
                "输入：处理给定格式的输入",
                "运算：对数据进行运算",
                "输出：输出要求的结果",
                "*代码格式：提高可读性",
                "*注释：能够进一步提高可读性",
                "*代码复用：减少重复代码，条理清晰",
                line_spacing=1,
                alignment="left",
            )
            .scale(0.5)
            .center()
            .to_edge(LEFT)
            .shift(0.5 * RIGHT)
        )

        other_line_1 = Text("注意 C/C++ 中数据类型的输入输出和各类转换。").scale(0.5)
        other_line_2 = (
            Text("尽量减少重复或不必要的运算，尤其是一些耗时巨大的运算。")
            .scale(0.5)
            .next_to(other_line_1, DOWN, buff=1)
            .align_to(other_line_1, LEFT)
        )
        other_line_3 = (
            Text("使用现成的函数时最好阅读其文档，明确输入类型和格式要求。")
            .scale(0.5)
            .next_to(other_line_2, DOWN, buff=1)
            .align_to(other_line_2, LEFT)
        )
        other_line_4 = (
            Text("写运算逻辑时尽量考虑全面，尤其是输入中可能的边界情况。")
            .scale(0.5)
            .next_to(other_line_3, DOWN, buff=1)
            .align_to(other_line_3, LEFT)
        )
        VGroup(other_line_1, other_line_2, other_line_3, other_line_4).center()

        # What is a program
        self.play(Write(t_title))
        self.wait(2)
        self.play(Transform(t_title, t_what))
        self.add(t_what)
        self.remove(t_title)
        self.wait(2)
        self.play(t_what.animate.to_edge(UL).set_fill(BLUE).scale(0.75))
        self.wait(2)
        for l in VGroup(l_1, l_2, l_3):
            self.play(Write(l))
            self.wait(2)
        self.play(FadeOut(VGroup(l_1, l_2, l_3)))

        # How to write a good program
        self.play(t_what.animate.center().set_fill(WHITE).scale(1 / 0.75))
        self.wait(2)
        self.play(Transform(t_what, t_how))
        self.add(t_how)
        self.remove(t_what)
        self.wait(2)
        self.play(t_how.animate.to_edge(UL).set_fill(BLUE).scale(0.75))
        self.play(Write(t_source), Write(code_source))
        self.wait(2)
        self.play(Write(p_list[0]))
        self.play(Circumscribe(code_source.code[0]))
        self.wait(2)
        self.play(Write(p_list[1]))
        self.play(Circumscribe(code_source.code[4:6]))
        self.wait(2)
        self.play(Write(p_list[2]))
        self.play(Circumscribe(code_source.code[6]))
        self.wait(2)
        self.play(Write(p_list[3]))
        self.play(
            Circumscribe(
                VGroup(
                    code_source.code[7][5:20],
                    code_source.code[8][5:20],
                    code_source.code[9][5:20],
                )
            )
        )
        self.wait(2)
        self.play(Write(p_list[4]))
        self.play(Circumscribe(code_source.code[10:13]))
        self.wait(2)
        self.play(Write(p_list[5]))
        self.play(FocusOn(code_source))
        self.wait(2)
        self.play(Write(p_list[6]))
        self.play(
            Circumscribe(
                VGroup(
                    code_source.code[7][20:26],
                    code_source.code[8][20:26],
                    code_source.code[9][20:26],
                )
            )
        )
        self.wait(2)
        self.play(Write(p_list[7]))
        self.wait(2)
        self.play(
            FadeOut(p_list, shift=LEFT),
            FadeOut(VGroup(t_source, code_source), shift=RIGHT),
        )
        self.wait(2)
        for l in VGroup(other_line_1, other_line_2, other_line_3, other_line_4):
            self.play(Write(l))
            self.wait(2)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait(2)


class Ending(Scene):
    def construct(self):
        t_ending = Text("感谢观看").scale(2)
        t_wish = Text("祝大家学习顺利").next_to(t_ending, DOWN)
        self.play(Write(t_ending))
        self.play(Write(t_wish))
        self.wait(2)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait(2)

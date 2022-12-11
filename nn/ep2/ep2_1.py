from manim import *
from ecommon import (
    get_title_screen,
    SCENE_WAIT,
    get_equations,
    get_highlight_box,
    rescale,
    retainTransform,
)

# Pooling
class ep2_1(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.1, "Pooling")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def max_pool(
        self,
        scale=0.5,
        label_spacing=0.5,
        arrow_spacing=0.02,
        image_size=(4, 4),
        pool_size=(2, 2),
    ):
        title = Text("Pooling")
        title.shift(3 * UP)

        subtitle = Text("Max pooling")
        subtitle.scale(0.6)
        subtitle.shift(2.6 * UP)

        equation = MathTex(
            r"\max(\{{in_{ih+m,jw+n} | n∪m⊆ℤ, 1 \leq m \leq h, 1 \leq n \leq w}\}) = out_{i+1,j+1}"
        )
        equation.scale(scale)

        self.play(Write(title), Write(subtitle))

        image_vals = [
            [random.randint(0, 5) for x in range(image_size[0])]
            for y in range(image_size[1])
        ]
        image = Matrix(image_vals)
        image_vals = sum(image_vals, [])

        img_label = Text("Image/Input")
        img_label.scale(scale)

        temp = Matrix(
            [
                [image_vals[x + y * image_size[0]] for x in range(pool_size[0])]
                for y in range(pool_size[1])
            ]
        ).set_color(YELLOW)

        new_image_size = (
            int(image_size[0] / pool_size[0]),
            int(image_size[1] / pool_size[1]),
        )
        new_image = Matrix(
            [[0 for x in range(new_image_size[0])] for y in range(new_image_size[1])]
        )
        new_image_label = Text("New image/Output")
        new_image_label.scale(scale)

        scene = VGroup(image, temp, new_image)
        scene.arrange(buff=3)
        scene.scale(scale)

        self.play(
            Write(image),
            Write(temp[1:3]),
            Write(new_image[1:3]),
        )

        # Sets image axis labels
        pool_rows = MathTex(r"h")
        pool_cols = MathTex(r"w")
        pool_rows.scale(scale)
        pool_cols.scale(scale)

        element_size = (
            image.get_width() / image_size[0],
            image.get_height() / image_size[1],
        )
        shift = (
            temp.get_width() / 2 - element_size[0] / 2,
            -temp.get_height() / 2 + element_size[1] / 2,
            0,
        )

        img_label.move_to(
            image.get_center()
            + [
                0,
                image.get_height() / 2 + img_label.get_height() / 2 + label_spacing,
                0,
            ]
        )
        new_image_label.move_to(
            new_image.get_center()
            + [
                0,
                new_image.get_height() / 2
                + new_image_label.get_height() / 2
                + label_spacing,
                0,
            ]
        )

        pool_rows.move_to(
            temp.get_center()
            - [
                temp.get_width() / 2 + pool_rows.get_width() / 2 + label_spacing / 4,
                0,
                0,
            ]
        )
        pool_cols.move_to(
            temp.get_center()
            - [
                0,
                temp.get_height() / 2 + pool_cols.get_height() / 2 + label_spacing / 4,
                0,
            ]
        )

        equation.move_to(
            temp.get_center()
            - [
                0,
                temp.get_height() / 2 + equation.get_height() / 2 + 2 * label_spacing,
                0,
            ]
        )

        self.play(
            Write(img_label),
            Write(new_image_label),
            Write(pool_rows),
            Write(pool_cols),
            Write(equation),
        )

        highlight = Rectangle(
            color=YELLOW, height=temp.get_height(), width=temp.get_width()
        )  # .set_fill(YELLOW, opacity=0.1)

        calculation = MathTex("placeholder")

        for yi, yni in zip(
            range(0, image_size[1], pool_size[1]), range(0, new_image_size[1])
        ):
            for xi, xni in zip(
                range(0, image_size[0], pool_size[0]), range(0, new_image_size[0])
            ):
                # Sets image index
                img_indx = xi + yi * image_size[0]

                # Sets calculation string
                max_of = "max("
                max_val = -1
                for y in range(pool_size[1]):
                    for x in range(pool_size[0]):
                        image_value = image_vals[(xi + x) + (yi + y) * image_size[0]]
                        max_of += str(image_value)
                        max_val = max(max_val, image_value)
                        if not (x == pool_size[0] - 1 and y == pool_size[1] - 1):
                            max_of += ","
                max_of += ")=" + str(max_val)

                # Sets pooled image index
                pooled_img_indx = xni + yni * new_image_size[0]

                if xi == 0 and yi == 0:
                    # Sets highlight
                    highlight.move_to(image[0][img_indx].get_center() + shift)

                    # Sets calculation string
                    calculation = MathTex(max_of)
                    calculation.scale(scale)
                    calculation.move_to(
                        equation.get_center()
                        - [
                            0,
                            equation.get_height() / 2
                            + calculation.get_height() / 2
                            + label_spacing,
                            0,
                        ]
                    )

                    # Sets arrow
                    arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        new_image[0][pooled_img_indx].get_center()
                        - [
                            new_image[0][pooled_img_indx].get_width() / 2
                            + arrow_spacing,
                            0,
                            0,
                        ],
                        stroke_width=5,
                        max_tip_length_to_length_ratio=0.07,
                    )
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(highlight),
                        Write(temp[0]),
                        Write(calculation),
                        Write(arrow),
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(image[0][img_indx].get_center() + shift)

                    # Sets receptive field
                    temp_vals = [
                        [
                            image_vals[(xi + x) + (yi + y) * image_size[0]]
                            for x in range(pool_size[0])
                        ]
                        for y in range(pool_size[1])
                    ]
                    new_temp = Matrix(temp_vals).set_color(YELLOW)
                    new_temp.scale(scale)
                    new_temp.move_to(temp.get_center())

                    # Sets calculation string
                    new_calculation = MathTex(max_of)
                    new_calculation.scale(scale)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        new_image[0][pooled_img_indx].get_center()
                        - [
                            new_image[0][pooled_img_indx].get_width() / 2
                            + arrow_spacing,
                            0,
                            0,
                        ],
                        stroke_width=5,
                        max_tip_length_to_length_ratio=0.07,
                    )
                    new_arrow.fade(0.5)

                    # Writes
                    self.play(
                        Transform(highlight, new_highlight),
                        Transform(temp[0], new_temp[0]),
                        Transform(calculation, new_calculation),
                        Transform(arrow, new_arrow),
                    )

                resul_obj = MathTex(str(max_val))
                resul_obj.scale(scale)
                resul_obj.move_to(new_image[0][pooled_img_indx].get_center())
                self.play(Write(resul_obj))

                self.wait()

    def construct(self):
        self.play_intro()

        self.max_pool()

        self.wait(3)

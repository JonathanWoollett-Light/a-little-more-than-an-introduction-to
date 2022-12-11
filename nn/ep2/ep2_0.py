from manim import *
from ecommon import (
    get_title_screen,
    SCENE_WAIT,
    get_equations,
    get_highlight_box,
    rescale,
    retainTransform,
)

# Convolution
class EpisodeScene(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.0, "Convolution")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_conv(
        self,
        scale=0.5,
        label_spacing=0.5,
        arrow_spacing=0.02,
        image_size=(3, 3),
        filter_size=(2, 2),
    ):
        title = Text("Convolution")
        title.shift(3 * UP)
        self.play(Write(title))

        componentwise_equation = MathTex(
            r"out_{i,j} = (in * filter)_{i,j} = \sum_{m=1}^h \sum_{n=1}^w in_{i+m,j+n} filter_{m,n} + b"
        )
        matrix_equation = MathTex(
            r"out = (in * filter) = in \cdot filter^T + b J_{h,w}"
        )
        equation = VGroup(componentwise_equation, matrix_equation)
        equation.arrange(DOWN)
        equation.scale(scale)

        image_vals = [
            [random.randint(0, 2) for x in range(image_size[0])]
            for y in range(image_size[1])
        ]
        image = Matrix(image_vals)
        image_vals = sum(image_vals, [])
        img_label = Text("Image/Input")
        img_label.scale(scale)

        # Sets image axis labels
        filter_rows = MathTex(r"h")
        filter_cols = MathTex(r"w")
        filter_rows.scale(scale)
        filter_cols.scale(scale)

        filt_vals = [
            [random.randint(0, 1) for x in range(filter_size[0])]
            for y in range(filter_size[1])
        ]
        filt = Matrix(filt_vals)
        filt_vals = sum(filt_vals, [])
        filt_label = Text("Filter/Kernel")
        filt_label.scale(scale)

        temp = Matrix(
            [[0 for x in range(filter_size[0])] for y in range(filter_size[1])]
        ).set_color(YELLOW)

        filt_group = VGroup(filt, MathTex("\odot"), temp)
        filt_group.arrange(buff=0.5)

        feature_size = (
            image_size[0] - filter_size[0] + 1,
            image_size[1] - filter_size[1] + 1,
        )
        feature = Matrix(
            [[0 for x in range(feature_size[0])] for y in range(feature_size[1])]
        )
        feature_label = Text("Feature/Output")
        feature_label.scale(scale)

        scene = VGroup(image, filt_group, feature)
        scene.arrange(buff=3)

        scene.scale(scale)

        calculation = VGroup(*[MathTex("placeholder") for i in range(filter_size[1])])

        self.play(
            Write(image), Write(filt_group[0:2]), Write(temp[1:3]), Write(feature[1:3])
        )

        highlight = Rectangle(
            color=YELLOW, height=filt.get_height(), width=filt.get_width()
        )  # .set_fill(YELLOW, opacity=0.1)

        element_size = [
            filt.get_width() / filter_size[0],
            filt.get_height() / filter_size[1],
        ]
        shift = [
            filt.get_width() / 2 - element_size[0] / 2,
            -filt.get_height() / 2 + element_size[1] / 2,
            0,
        ]

        img_label.move_to(
            image.get_center()
            + [
                0,
                image.get_height() / 2
                + img_label.get_height() / 2
                + label_spacing
                + element_size[1],
                0,
            ]
        )
        filt_label.move_to(
            filt.get_center()
            + [
                0,
                filt.get_height() / 2
                + filt_label.get_height() / 2
                + label_spacing
                + element_size[1],
                0,
            ]
        )
        feature_label.move_to(
            feature.get_center()
            + [
                0,
                feature.get_height() / 2
                + feature_label.get_height() / 2
                + label_spacing
                + element_size[1],
                0,
            ]
        )

        filter_rows.move_to(
            filt.get_center()
            - [
                filt.get_width() / 2 + filter_rows.get_width() / 2 + label_spacing / 4,
                0,
                0,
            ]
        )
        filter_cols.move_to(
            filt.get_center()
            - [
                0,
                filt.get_height() / 2
                + filter_cols.get_height() / 2
                + label_spacing / 4,
                0,
            ]
        )

        equation.move_to(
            filt_group.get_center()
            - [
                0,
                filt_group.get_height() / 2 + equation.get_height() / 2 + label_spacing,
                0,
            ]
        )

        self.play(
            Write(img_label),
            Write(filt_label),
            Write(feature_label),
            Write(filter_rows),
            Write(filter_cols),
            Write(equation),
        )

        written = []

        for yi in range(0, feature_size[1]):
            for xi in range(0, feature_size[0]):
                # Gets index in image
                image_indx = xi + yi * image_size[0]

                # Gets and sets values in local receptive field
                temp_vals = [
                    [
                        image_vals[(xi + x) + (yi + y) * image_size[0]]
                        for x in range(filter_size[0])
                    ]
                    for y in range(filter_size[1])
                ]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temp.get_center())

                # Gets result and calculation string
                multiplying = ["" for i in range(filter_size[1])]
                result = 0
                for indx, y in enumerate(range(filter_size[1])):
                    for x in range(filter_size[0]):
                        filter_value = filt_vals[x + y * filter_size[0]]
                        image_value = image_vals[(xi + x) + (yi + y) * image_size[0]]

                        multiplying[indx] += (
                            "(" + str(filter_value) + "\\cdot" + str(image_value) + ")"
                        )

                        result += filter_value * image_value

                        if x == filter_size[0] - 1 and y == filter_size[1] - 1:
                            multiplying[indx] += " = " + str(result)
                        else:
                            multiplying[indx] += "+"

                # Gets index in feature
                feature_indx = xi + yi * feature_size[0]

                if xi == 0 and yi == 0:
                    # Sets highlight
                    highlight.move_to(image[0][image_indx].get_center() + shift)

                    # Sets calculation string
                    calculation = VGroup(*[MathTex(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN, buff=0.2)
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

                    # Sets arrow to feature
                    arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        feature[0][feature_indx].get_center()
                        - [
                            feature[0][feature_indx].get_width() / 2 + arrow_spacing,
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
                        Transform(temp[0], new_temp[0]),
                        Write(calculation),
                        Write(arrow),
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(image[0][image_indx].get_center() + shift)

                    # Sets calculation string
                    new_calculation = VGroup(*[MathTex(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN, buff=0.2)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow to feature
                    new_arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        feature[0][feature_indx].get_center()
                        - [
                            feature[0][feature_indx].get_width() / 2 + arrow_spacing,
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

                # Sets and writes result
                resul_obj = MathTex(str(result))
                resul_obj.scale(scale)
                resul_obj.move_to(feature[0][feature_indx].get_center())
                self.play(Write(resul_obj))
                written.append(resul_obj)

                self.wait()

        written = VGroup(*written)

        self.play(Uncreate(arrow), Uncreate(calculation), Uncreate(highlight))

        return (
            image,
            feature,
            filt,
            temp,
            image_size,
            filter_size,
            image_vals,
            filt_vals,
            equation,
            written,
        )

    def play_padding_conv(
        self,
        image,
        feature,
        filt,
        temp,
        image_size,
        filter_size,
        image_vals,
        filt_vals,
        equation,
        label_spacing=0.5,
        scale=0.5,
        arrow_spacing=0.02,
    ):
        # Gets highlight
        highlight = Rectangle(
            color=YELLOW, height=filt.get_height(), width=filt.get_width()
        )

        # Sets and writes subtitle
        subtitle = Text("Zero padding")
        subtitle.scale(0.6)
        subtitle.shift(2.6 * UP)
        self.play(Write(subtitle))

        # Sets new image size and buffer
        buffer = (int(filter_size[0] / 2), int(filter_size[1] / 2))
        padded_image_size = [
            image_size[0] + 2 * buffer[0],
            image_size[1] + 2 * buffer[1],
        ]

        # Gets and sets zero-padded image
        padded_image_vals = []
        for y in range(0, padded_image_size[1]):
            holder = []
            for x in range(0, padded_image_size[0]):
                if (
                    y < buffer[1]
                    or x < buffer[0]
                    or y > image_size[1]
                    or x > image_size[0]
                ):
                    holder.append(0)
                else:
                    holder.append(
                        image_vals[(x - buffer[0]) + (y - buffer[1]) * image_size[0]]
                    )
            padded_image_vals.append(holder)
        padded_image = Matrix(padded_image_vals)
        padded_image.scale(scale)
        padded_image.move_to(image.get_center())

        # Sets group containg all the padding zeros
        padding = []
        for y in range(0, padded_image_size[1]):
            for x in range(0, padded_image_size[0]):
                if (
                    y < buffer[1]
                    or x < buffer[0]
                    or y > image_size[1]
                    or x > image_size[0]
                ):
                    padding.append(padded_image[0][x + y * padded_image_size[0]])
        padding = VGroup(*padding)

        # Sets non padded image holder
        image_holder = image.copy()

        # Transforms brackets but retains copy of old brackets
        image_brackets = retainTransform(self, image[1:3], padded_image[1:3])

        # Writes zero padding
        self.play(Write(padding))

        # Flattens image values
        image_vals = sum(padded_image_vals, [])

        # Sets new feature
        feature_size = (
            padded_image_size[0] - filter_size[0] + 1,
            padded_image_size[1] - filter_size[1] + 1,
        )
        padded_feature = Matrix(
            [
                [
                    0 for x in range(feature_size[0])
                ]  # `0` simply being used as placeholder value
                for y in range(feature_size[1])
            ]
        )
        padded_feature.scale(scale)
        padded_feature.move_to(feature.get_center())

        # Transforms brackets but retains copy of old brackets
        feature_brackets = retainTransform(self, feature[1:3], padded_feature[1:3])

        # Sets element size and needed highlight shift
        element_size = [
            filt.get_width() / filter_size[0],
            filt.get_height() / filter_size[1],
        ]
        shift = [
            filt.get_width() / 2 - element_size[0] / 2,
            -filt.get_height() / 2 + element_size[1] / 2,
            0,
        ]

        # Defines container for all newly written feature values
        written = []

        for yi in range(0, feature_size[1]):
            for xi in range(0, feature_size[0]):
                # Gets image index
                image_indx = xi + yi * padded_image_size[0]

                # Gets  and sets local receptive field values
                temp_vals = [
                    [
                        image_vals[(xi + x) + (yi + y) * padded_image_size[0]]
                        for x in range(filter_size[0])
                    ]
                    for y in range(filter_size[1])
                ]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temp.get_center())

                # Defines calculation string
                multiplying = ["" for i in range(filter_size[1])]
                result = 0

                for indx, y in enumerate(range(filter_size[1])):
                    for x in range(filter_size[0]):
                        filter_value = filt_vals[x + y * filter_size[0]]
                        image_value = image_vals[
                            (xi + x) + (yi + y) * padded_image_size[0]
                        ]

                        multiplying[indx] += (
                            "(" + str(filter_value) + "\\cdot" + str(image_value) + ")"
                        )

                        result += filter_value * image_value

                        if x == filter_size[0] - 1 and y == filter_size[1] - 1:
                            multiplying[indx] += " = " + str(result)
                        else:
                            multiplying[indx] += "+"

                feature_indx = xi + yi * feature_size[0]

                if xi == 0 and yi == 0:
                    # Sets highlight
                    highlight.move_to(padded_image[0][image_indx].get_center() + shift)

                    # Sets calculation
                    calculation = VGroup(*[MathTex(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN, buff=0.2)
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
                        padded_feature[0][feature_indx].get_center()
                        - [
                            padded_feature[0][feature_indx].get_width() / 2
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
                        Write(arrow),
                        Write(calculation),
                        Write(highlight),
                        Transform(temp[0], new_temp[0]),
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(
                        padded_image[0][image_indx].get_center() + shift
                    )

                    # Sets calculation
                    new_calculation = VGroup(*[MathTex(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN, buff=0.2)
                    new_calculation.move_to(calculation.get_center())
                    self.play()

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        padded_feature[0][feature_indx].get_center()
                        - [
                            padded_feature[0][feature_indx].get_width() / 2
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
                        Transform(arrow, new_arrow),
                        Transform(calculation, new_calculation),
                        Transform(highlight, new_highlight),
                        Transform(temp[0], new_temp[0]),
                    )

                # Writes padding result
                if (
                    yi == 0
                    or xi == 0
                    or xi == feature_size[0] - 1
                    or yi == feature_size[1] - 1
                ):
                    resul_obj = MathTex(str(result))
                    resul_obj.scale(scale)
                    resul_obj.move_to(padded_feature[0][feature_indx].get_center())
                    self.play(Write(resul_obj))
                    written.append(resul_obj)
                self.wait()

        # Uncreates
        self.play(Uncreate(subtitle))
        self.play(Uncreate(arrow), Uncreate(highlight), Uncreate(calculation))
        self.play(Uncreate(padding), Uncreate(VGroup(*written)))
        self.play(
            ReplacementTransform(padded_image[1:3], image_brackets),
            ReplacementTransform(padded_feature[1:3], feature_brackets),
        )

        return image_holder

    def play_channels_conv(
        self,
        image,
        feature,
        filt,
        temp,
        image_vals,
        filt_vals,
        equation,
        written,
        image_size=(3, 3),
        filter_size=(2, 2),
        layers=3,
        label_spacing=0.5,
        scale=0.5,
        arrow_spacing=0.02,
    ):
        # Uncreates all feature values
        self.play(Uncreate(written))

        # Sets subtitle
        subtitle = Text("Channels")
        subtitle.scale(0.6)
        subtitle.shift(2.6 * UP)

        # Sets filter depth label
        filter_depth = MathTex(r"d")
        filter_depth.scale(scale)
        filter_depth.move_to(
            filt.get_center()
            - [
                filt.get_width() / 2 + filter_depth.get_width() / 2 + label_spacing / 4,
                filt.get_height() / 2
                + filter_depth.get_height() / 2
                + label_spacing / 4,
                0,
            ]
        )

        # Sets equation
        new_equation = MathTex(
            r"out_{i,j} = (in * filters)_{i,j} = \sum_{l=1}^d \sum_{m=1}^h \sum_{n=1}^w in_{i+m,j+n,l} \cdot filter_{m,n,l} + b"
        )
        new_equation.scale(scale)
        new_equation.move_to(equation.get_center())

        # Writes subtitle, depth label and equation
        self.play(
            Write(subtitle),
            Write(filter_depth),
            ReplacementTransform(equation, new_equation),
        )

        # Sets and writes new layers to image, filter and local receptive field
        images = VGroup(*[image.copy() for i in range(layers)])
        lines = set_layers(images)

        filters = VGroup(*[filt] + [filt.copy() for i in range(layers - 1)])
        lines = set_layers(filters)

        temps = VGroup(*[temp] + [temp.copy() for i in range(layers - 1)])
        lines = set_layers(temps)

        self.play(
            Write(images[1:layers]), Write(filters[1:layers]), Write(temps[1:layers])
        )

        # Sets feature size
        feature_size = (
            image_size[0] - filter_size[0] + 1,
            image_size[1] - filter_size[1] + 1,
        )

        # Sets element size and highlight shift
        element_size = [
            filt.get_width() / filter_size[0],
            filt.get_height() / filter_size[1],
        ]
        shift = [
            filt.get_width() / 2 - element_size[0] / 2,
            -filt.get_height() / 2 + element_size[1] / 2,
            0,
        ]

        # Sets highlight
        highlight = Rectangle(
            color=YELLOW, height=filt.get_height(), width=filt.get_width()
        )

        for yi in range(0, feature_size[1]):
            for xi in range(0, feature_size[0]):
                # Sets image index
                image_indx = xi + yi * image_size[0]

                # Sets local receptive field
                temp_vals = [
                    [
                        image_vals[(xi + x) + (yi + y) * image_size[0]]
                        for x in range(filter_size[0])
                    ]
                    for y in range(filter_size[1])
                ]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temps[0].get_center())
                new_temps = VGroup(*[new_temp.copy() for i in range(layers)])
                lines = set_layers(new_temps)

                # Define calculation string
                multiplying = ["" for i in range(layers)]
                result = 0
                for z in range(layers):
                    multiplying[z] += "["
                    for y in range(filter_size[1]):
                        for x in range(filter_size[0]):
                            filter_value = filt_vals[x + y * filter_size[0]]
                            image_value = image_vals[
                                (xi + x) + (yi + y) * image_size[0]
                            ]

                            multiplying[z] += (
                                "("
                                + str(filter_value)
                                + "\\cdot"
                                + str(image_value)
                                + ")"
                            )

                            result += filter_value * image_value
                            if x == filter_size[0] - 1 and y == filter_size[1] - 1:
                                multiplying[z] += "]"
                                if z == layers - 1:
                                    multiplying[z] += " = " + str(result)
                            else:
                                multiplying[z] += "+"

                # Sets feature index
                feature_indx = xi + yi * feature_size[0]

                if xi == 0 and yi == 0:
                    # Sets highlight
                    highlight.move_to(image[0][image_indx].get_center() + shift)
                    highlights = VGroup(*[highlight.copy() for i in range(layers)])
                    lines = set_layers(highlights)

                    # Sets calculation
                    calculation = VGroup(*[MathTex(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN, buff=0.2)
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
                        feature[0][feature_indx].get_center()
                        - [
                            feature[0][feature_indx].get_width() / 2 + arrow_spacing,
                            0,
                            0,
                        ],
                        stroke_width=5,
                        max_tip_length_to_length_ratio=0.07,
                    )
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(highlights),
                        Transform(temps, new_temps),
                        Write(calculation),
                        Write(arrow),
                    )
                else:
                    # Sets highlight
                    distance = (
                        image[0][image_indx].get_center() - highlights[0].get_center()
                    )
                    new_highlights = highlights.copy()
                    new_highlights.shift(distance + shift)

                    # Sets calculation
                    new_calculation = VGroup(*[MathTex(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN, buff=0.2)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()
                        + [temp.get_width() / 2 + arrow_spacing, 0, 0],
                        feature[0][feature_indx].get_center()
                        - [
                            feature[0][feature_indx].get_width() / 2 + arrow_spacing,
                            0,
                            0,
                        ],
                        stroke_width=5,
                        max_tip_length_to_length_ratio=0.07,
                    )
                    new_arrow.fade(0.5)

                    # Writes
                    self.play(
                        Transform(highlights, new_highlights),
                        Transform(temps, new_temps),
                        Transform(calculation, new_calculation),
                        Transform(arrow, new_arrow),
                    )
                # Writes feature value
                if (
                    yi == 0
                    or xi == 0
                    or xi == feature_size[0] - 1
                    or yi == feature_size[1] - 1
                ):
                    resul_obj = MathTex(str(result))
                    resul_obj.scale(scale)
                    resul_obj.move_to(feature[0][feature_indx].get_center())
                    self.play(Write(resul_obj))
                self.wait()

    def construct(self):
        self.play_intro()

        (
            image,
            feature,
            filt,
            temp,
            image_size,
            filter_size,
            image_vals,
            filt_vals,
            equation,
            written,
        ) = self.play_conv()

        image = self.play_padding_conv(
            image,
            feature,
            filt,
            temp,
            image_size,
            filter_size,
            image_vals,
            filt_vals,
            equation,
        )

        self.play_channels_conv(
            image, feature, filt, temp, image_vals, filt_vals, equation, written
        )

        self.wait(3)

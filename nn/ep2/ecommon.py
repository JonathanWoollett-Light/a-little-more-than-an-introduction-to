import os
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from manim import *
from scommon import (
    get_equations,
    get_highlight_box,
    get_title_screen,
    rescale,
    retainTransform,
)

UP_SHIFT = 2.4


def get_explicit_conv_net(
    in_shape,  # (y,x)/(m,n)
    conv_layers,
    dense_layers,
    scale=0.4,
    arrow_spacing=0.05,
    layer_spacing=1,
    circle_spacing=0.1,
):
    # Adds input
    inputs = VGroup(Matrix([[str(in_shape[1]) + "\\times" + str(in_shape[0])]]))
    inputs.scale(scale)

    # Adds conv layers
    layers = [inputs]
    layers += [
        Matrix([[str(i) + "\\times" + "(" + str(m) + "\\times" + str(n) + ")"]]).scale(
            scale
        )
        for (i, m, n) in conv_layers
    ]
    circles = []
    for layer in dense_layers:
        num = Text(str(layer)).scale(scale)
        layers += num

    layers = VGroup(*layers)
    layers.arrange(buff=layer_spacing)

    circles = []
    for index in range(len(dense_layers)):
        circ = Circle(
            radius=layers[index + len(conv_layers) + 1].get_height() / 2
            + circle_spacing,
            color=WHITE,
            stroke_width=2,
        )
        circ.move_to(layers[index + len(conv_layers) + 1].get_center())
        circles += circ

    # Adds arrows between layers
    arrows = [
        Arrow(
            layers[i].get_center() + [layers[i].get_width() / 2 + arrow_spacing, 0, 0],
            layers[i + 1].get_center()
            - [layers[i + 1].get_width() / 2 + arrow_spacing, 0, 0],
        )
        for i in range(len(layers) - 1)
    ]

    net = VGroup(layers, VGroup(*arrows), VGroup(*circles))
    net.center()
    return net


def setup(scale, h_buff, distance=0.3, buff=0.4):
    # 3x3
    a1 = Matrix([[1, 1, 0], [0, 1, 0], [0, 1, 1]], h_buff=h_buff)

    # 1st conv layer
    # ---------------------------------
    # 2x2
    f1 = VGroup(
        Matrix([[1, 1], [0, 0]], h_buff=h_buff).set_color(RED),
        Matrix([[1, 0], [0, 0]], h_buff=h_buff).set_color(RED),
    )
    f1.arrange(DOWN)

    b1 = VGroup(MathTex("-2", color=BLUE), MathTex("-1", color=BLUE))
    b1.arrange(DOWN)

    z1 = VGroup(
        Matrix([[0, -1], [-1, -1]], h_buff=2 * h_buff),
        Matrix([[0, 0], [-1, 0]], h_buff=2 * h_buff),
    )
    set_layers(z1, distance=distance)

    # Can copy bc ReLU is same when all zs >=0
    a2 = VGroup(
        Matrix([[0, 1], [1, 1]], h_buff=h_buff), Matrix([[0, 0], [1, 0]], h_buff=h_buff)
    )
    set_layers(a2, distance=distance)

    # 2nd conv layer
    # ---------------------------------
    # 1x2 (1 rows, 2 cols)
    f2 = VGroup(
        VGroup(
            Matrix([[0, 1]], h_buff=h_buff).set_color(RED),
            Matrix([[1, 0]], h_buff=h_buff).set_color(RED),
        ),
        VGroup(
            Matrix([[1, 0]], h_buff=h_buff).set_color(RED),
            Matrix([[0, 1]], h_buff=h_buff).set_color(RED),
        ),
        VGroup(
            Matrix([[1, 1]], h_buff=h_buff).set_color(RED),
            Matrix([[1, 1]], h_buff=h_buff).set_color(RED),
        ),
    )
    for f in f2:
        set_layers(f, distance=distance)
    f2.arrange(DOWN)

    b2 = VGroup(
        MathTex("-1", color=BLUE), MathTex("-1", color=BLUE), MathTex("-2", color=BLUE)
    )
    b2.arrange(DOWN)

    z2 = VGroup(Matrix([[1], [2]]), Matrix([[0], [1]]), Matrix([[1], [3]]))
    set_layers(z2, distance=distance)

    # ReLU
    a3 = z2.copy()

    # 1st dense layer
    # ---------------------------------
    w1 = Matrix([[1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1]], h_buff=h_buff).set_color(RED)

    b3 = Matrix([[-1], [-3]], h_buff=h_buff).set_color(BLUE)

    z3 = Matrix([[1], [3]])
    a4 = z3.copy()  # ReLU

    everything = VGroup(a1, f1, b1, z1, a2, f2, b2, z2, a3, w1, b3, z3, a4)
    everything.arrange(buff=buff)
    everything.scale(scale)

    starting = VGroup(
        a1,
        f1,
        z1[0][1:3],
        z1[1][1:3],
        b1,
        a2[0][1:3],
        a2[1][1:3],
        f2,
        z2[0][1:3],
        z2[1][1:3],
        z2[2][1:3],
        b2,
        a3[0][1:3],
        a3[1][1:3],
        a3[2][1:3],
        w1,
        z3[1:3],
        b3,
        a4[1:3],
    )

    return (a1, f1, b1, z1, a2, f2, b2, z2, a3, w1, b3, z3, a4, everything, starting)


# Given some items, aligns them along z axis.
def set_layers(layers, distance=0.1, gradient=0.9, scaling=1):
    scale = 1
    perspective_lines = []
    opaqueness = 1
    for i in range(len(layers) - 1):
        layers[i + 1].fade(1 - opaqueness)

        layers[i + 1].scale(scale)

        layers[i + 1].move_to(
            layers[i].get_center() + (distance * UP) + (distance * RIGHT)
        )

        h2s, w2s = layers[i].get_height() / 2, layers[i].get_width() / 2
        h2e, w2e = layers[i + 1].get_height() / 2, layers[i + 1].get_width() / 2

        cs = layers[i].get_center()
        xs, ys, zs = cs[0], cs[1], cs[2]
        ce = layers[i + 1].get_center()
        xe, ye, ze = ce[0], ce[1], ce[2]

        lines = VGroup(
            DashedLine([xs + w2s, ys + h2s, zs], [xe + w2e, ye + h2e, ze]),
            DashedLine([xs + w2s, ys - h2s, zs], [xe + w2e, ye - h2e, ze]),
            DashedLine([xs - w2s, ys + h2s, zs], [xe - w2e, ye + h2e, ze]),
            DashedLine([xs - w2s, ys - h2s, zs], [xe - w2e, ye - h2e, ze]),
        )
        lines.fade(1 - opaqueness)

        perspective_lines.append(lines)

        scale *= scaling
        opaqueness *= gradient
        distance *= scaling

    return VGroup(*perspective_lines)


# TODO
# - Regularization (L2 + dropout)
# - Initialization
# - Different cost functions (quadratic + crossentropy)
# - Different activations (sigmoid + tanh + softmax + relu + lrelu)


def get_matrix_conv_net(
    conv_layers,
    dense_layers,
    input_scale=0.4,
    filter_scale=0.7,
    arrow_spacing=0.1,
    layer_spacing=2,
    neuron_spacing=0.2,
    neuron_radius=0.1,
    in_shape=(0, 0),
):
    # Adds input#
    inputs = VGroup(*[MathTex("placeholder")])
    if in_shape == (0, 0):
        inputs = VGroup(
            Matrix(
                [
                    ["a_{1,1,1}", "\\dots", "a_{1,1,n_1}"],
                    ["\\vdots", "\\ddots", "\\vdots"],
                    ["a_{1,m_1,1}", "\\dots", "a_{1,m_1,n_1}"],
                ],
                h_buff=1.8,
                v_buff=1.8,
            )
        )

    else:
        inputs = VGroup(
            Matrix(
                [
                    [
                        "a_{" + str(x + 1) + "," + str(y + 1) + "}"
                        for x in range(in_shape[1])
                    ]
                    for y in range(in_shape[0])
                ]
            )
        )

    inputs.scale(input_scale)

    filt = Matrix([["\\ddots"]])
    filt.scale(filter_scale)

    # Adds conv layers
    layers = [VGroup(*[filt.copy() for c in range(layer)]) for layer in conv_layers]
    for layer in layers:
        set_layers(layer)
    layers.insert(0, inputs)
    for i in range(1, len(layers)):
        layers[i].shift(
            [
                layers[i - 1][0].get_x()
                + layers[i - 1][0].get_width() / 2
                + layers[i][0].get_width() / 2
                + layer_spacing,
                0,
                0,
            ]
        )

    # Adds dense layers
    connections = []
    for i in range(len(dense_layers)):
        dense = VGroup(
            *[
                Circle(radius=neuron_radius, stroke_color=WHITE, stroke_width=1)
                for j in range(dense_layers[i])
            ]
        )
        dense.arrange(DOWN, buff=neuron_spacing)

        if i == 0:
            dense.shift(
                [
                    layers[-1][0].get_x()
                    + layers[-1][0].get_width() / 2
                    + dense.get_width() / 2
                    + layer_spacing,
                    0,
                    0,
                ]
            )
        else:
            dense.shift(
                [
                    layers[-1].get_x()
                    + layers[-1].get_width() / 2
                    + dense.get_width() / 2
                    + layer_spacing / 2,
                    0,
                    0,
                ]
            )

        layers.append(dense)
        # Not first dense layer
        if i != 0:
            layer_connections = VGroup(
                *[
                    Line(
                        layers[-2][j].get_center()
                        + [layers[-2][j].get_width() / 2, 0, 0],
                        layers[-1][k].get_center()
                        - [layers[-1][k].get_width() / 2, 0, 0],
                        stroke_width=2,
                    )
                    for j in range(len(layers[-2]))
                    for k in range(len(layers[-1]))
                ]
            )
            connections.append(layer_connections)

    # Adds arrows between conv layers and first dense layer
    arrows = [
        Arrow(
            layers[i][0].get_center()
            + [layers[i][0].get_width() / 2 + arrow_spacing, 0, 0],
            layers[i + 1][0].get_center()
            - [layers[i + 1][0].get_width() / 2 + arrow_spacing, 0, 0],
        )
        for i in range(0, len(conv_layers))
    ]
    l_conv = len(conv_layers)
    arrows.append(
        Arrow(
            layers[l_conv][0].get_center()
            + [layers[l_conv][0].get_width() / 2 + arrow_spacing, 0, 0],
            layers[l_conv + 1].get_center()
            - [layers[l_conv + 1].get_width() / 2 + arrow_spacing, 0, 0],
        )
    )

    net = VGroup(VGroup(*layers), VGroup(*arrows), VGroup(*connections))
    net.center()
    return net


def get_denseish_conv_net(
    conv_layers,
    dense_layers,
    input_scale=0.3,
    filter_scale=0.2,
    filter_spacing=0.1,
    neuron_spacing=0.1,
    neuron_radius=0.05,
    layer_spacing=1,
):
    inputs = VGroup(
        Matrix(
            [
                ["a_{1,1,1}", "\\dots", "a_{1,1,n_1}"],
                ["\\vdots", "\\ddots", "\\vdots"],
                ["a_{1,m_1,1}", "\\dots", "a_{1,m_1,n_1}"],
            ],
            h_buff=1.8,
            v_buff=1.8,
        )
    )
    inputs.scale(input_scale)

    layers = [inputs]
    conv_layers.insert(0, 1)

    connections = []

    filt = Matrix([["\\ddots"]])
    filt.scale(filter_scale)

    lines = []

    max_filters = max(conv_layers)

    # Adds conv filter
    for i in range(1, len(conv_layers)):
        filters = VGroup(*[filt.copy() for t in range(conv_layers[i])])

        max_scale = max_filters / conv_layers[i]  # e.g. 1->128=128/1 or 64->128=128/64
        spacing = max_scale * (filter_spacing + filt.get_height()) - filt.get_height()
        filters.arrange(DOWN, buff=spacing)

        # line = Line([0,0,0],[0,spacing,0],stroke_width=0.5)
        # line.move_to(layers[i].get_center())
        # line.shift([2,0,0])
        # lines.append(line)

        filters.move_to(layers[-1].get_center())
        filters.shift(
            [layers[-1].get_width() / 2 + filters.get_width() / 2 + layer_spacing, 0, 0]
        )

        layers.append(filters)

    # Adds conv connections
    for i in range(len(conv_layers) - 1):
        next_scale = int(conv_layers[i + 1] / conv_layers[i])
        layer_connections = VGroup(
            *[
                Line(
                    layers[i][k].get_center() + [layers[i][k].get_width() / 2, 0, 0],
                    layers[i + 1][next_scale * k + j].get_center()
                    - [layers[i + 1][next_scale * k + j].get_width() / 2, 0, 0],
                    stroke_width=0.5,
                )
                for j in range(next_scale)
                for k in range(conv_layers[i])
            ]
        )
        connections.append(layer_connections)

    # Adds dense layers
    for i in range(len(dense_layers)):
        dense = VGroup(
            *[
                Circle(radius=neuron_radius, stroke_color=WHITE, stroke_width=1)
                for j in range(dense_layers[i])
            ]
        )
        dense.arrange(DOWN, buff=neuron_spacing)

        dense.move_to(layers[-1].get_center())
        dense.shift(
            [layers[-1].get_width() / 2 + dense.get_width() / 2 + layer_spacing, 0, 0]
        )

        layers.append(dense)

        layer_connections = VGroup(
            *[
                Line(
                    layers[-2][j].get_center() + [layers[-2][j].get_width() / 2, 0, 0],
                    layers[-1][k].get_center() - [layers[-1][k].get_width() / 2, 0, 0],
                    stroke_width=0.5,
                )
                for j in range(len(layers[-2]))
                for k in range(len(layers[-1]))
            ]
        )
        connections.append(layer_connections)

    # lines = VGroup(*lines)
    net = VGroup(VGroup(*layers), VGroup(*connections))
    net.center()
    return net

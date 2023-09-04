# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


def source_a():
    ...


def sink_b(arg):
    ...


def source_c():
    ...


def sink_d(arg):
    ...


def transform_x(arg):
    pass


def transform_y(arg):
    pass


def transform_z(arg):
    pass


def taint_with_transform_x():
    alpha = source_a()
    return transform_x(alpha)


def transform_x_obscure(arg):
    ...


def taint_with_transform_x_obscure():
    alpha = source_a()
    return transform_x_obscure(alpha)


def transform_x_skip_obscure(arg):
    ...


def taint_with_transform_x_skip_obscure():
    alpha = source_a()
    return transform_x_skip_obscure(alpha)


def taint_with_transform_yx():
    alpha = source_a()
    beta = transform_x(alpha)
    return transform_y(beta)


def no_source_taint_with_transform_z():
    alpha = source_a()
    return transform_z(alpha)


def no_source_taint_with_transform_zx():
    alpha = source_a()
    beta = transform_x(alpha)
    return transform_z(beta)


def a_to_b_no_issue():
    alpha = source_a()
    sink_b(alpha)


def a_to_x_to_b_issue():
    alpha = source_a()
    beta = transform_x(alpha)
    sink_b(beta)


def a_to_x_to_x_b_no_issue():
    alpha = source_a()
    beta = transform_x(alpha)
    gamma = transform_x(beta)
    sink_b(gamma)


def c_to_d_issue():
    alpha = source_c()
    sink_d(alpha)


def c_to_x_to_d_no_issue():
    alpha = source_c()
    beta = transform_x(alpha)
    sink_d(beta)


def a_to_z_to_y_to_b_no_issue():
    alpha = source_a()
    beta = transform_z(alpha)
    gamma = transform_y(beta)
    sink_b(gamma)


def a_to_y_to_z_to_b_issue():
    alpha = source_a()
    beta = transform_y(alpha)
    gamma = transform_z(beta)
    sink_b(gamma)


def sink_taint_with_transform_x(arg):
    alpha = transform_x(arg)
    sink_b(alpha)


def no_sink_taint_with_transform_y(arg):
    # TODO(T133358142): Do not output ExtraTraceSink when
    # there is no tito in the model
    alpha = transform_y(arg)
    sink_b(alpha)


def sink_taint_with_transform_yz(arg):
    alpha = transform_y(arg)
    beta = transform_z(alpha)
    sink_b(beta)


def tito_with_transform_x(arg):
    return transform_x(arg)


def tito_with_transform_yz(arg):
    alpha = transform_y(arg)
    return transform_z(alpha)


def nested_tito_transform_x(arg):
    return tito_with_transform_x(arg)


def source_taint_via_tito_tranform_yz():
    alpha = source_a()
    return tito_with_transform_yz(alpha)


def sink_taint_via_tito_transform_yz(arg):
    alpha = tito_with_transform_yz(arg)
    sink_b(alpha)


def ayz_to_b_issue():
    alpha = source_taint_via_tito_tranform_yz()
    sink_b(alpha)


def a_to_yzb_issue():
    alpha = source_a()
    sink_taint_with_transform_yz(alpha)


def source_taint_with_transform_y():
    alpha = source_a()
    return transform_y(alpha)


def sink_taint_with_transform_z(arg):
    alpha = transform_z(arg)
    sink_b(alpha)


def ay_to_zb_issue():
    alpha = source_taint_with_transform_y()
    sink_taint_with_transform_z(alpha)


def ay_to_z_to_b_issue():
    alpha = source_taint_with_transform_y()
    beta = transform_z(alpha)
    sink_b(beta)


def a_to_yz_to_b_issue():
    alpha = source_a()
    beta = tito_with_transform_yz(alpha)
    sink_b(beta)


def a_to_yz_to_d_no_issue():
    alpha = source_a()
    beta = tito_with_transform_yz(alpha)
    sink_d(beta)


def c_to_yz_to_b_no_issue():
    alpha = source_c()
    beta = tito_with_transform_yz(alpha)
    sink_b(beta)


def a_to_y_zb_issue():
    alpha = source_a()
    beta = transform_y(alpha)
    sink_taint_with_transform_z(beta)


def ax_to_zb_no_issue():
    alpha = taint_with_transform_x_obscure()
    sink_taint_with_transform_z(alpha)


def issue_with_repeated_transforms():
    alpha = taint_with_transform_yx()
    sink_taint_with_transform_yz(alpha)


def test_infinite_loop():
    x = source_a()
    while True:
        x = tito_with_transform_x(x)

        if x:
            return x


# Sanitizers and transforms interaction tests


def sanitize_source_a_tito(arg):
    return arg


def sanitize_source_c_tito(arg):
    return arg


def sanitize_sink_b_tito(arg):
    return arg


def sanitize_sink_d_tito(arg):
    return arg


def sanitize_a_transform_x(arg):
    alpha = sanitize_source_a_tito(arg)
    return transform_x(alpha)


def sanitize_a_transform_x_sanitize_c_transform_y(arg):
    alpha = sanitize_a_transform_x(arg)
    beta = sanitize_source_c_tito(alpha)
    return transform_y(beta)


# ... -> source sanitizer -> ... (no transforms)


def c_to_sanitize_c_to_d_no_issue():
    alpha = source_c()
    beta = sanitize_source_c_tito(alpha)
    sink_d(beta)


# ... -> transforms -> source sanitizer -> ...


def a_to_x_to_sanitize_a_to_b_issue():
    alpha = source_a()
    beta = transform_x(alpha)
    gamma = sanitize_source_a_tito(beta)
    sink_b(gamma)


def transform_x_sanitize_a_tito(arg):
    alpha = transform_x(arg)
    return sanitize_source_a_tito(alpha)


def a_to_x_sanitize_a_to_b_issue():
    alpha = source_a()
    beta = transform_x_sanitize_a_tito(alpha)
    sink_b(beta)


def sanitize_a_sink_b_taint(arg):
    alpha = sanitize_source_a_tito(arg)
    sink_b(alpha)


def a_to_x_to_sanitize_a_b_issue():
    alpha = source_a()
    beta = transform_x(alpha)
    sanitize_a_sink_b_taint(beta)


def ax_to_sanitize_a_b_issue():
    alpha = taint_with_transform_x()
    sanitize_a_sink_b_taint(alpha)


def transform_x_sanitize_a_sink_b_taint(arg):
    alpha = transform_x(arg)
    beta = sanitize_source_a_tito(alpha)
    sink_b(beta)


def a_to_x_sanitize_a_b_issue():
    alpha = source_a()
    transform_x_sanitize_a_sink_b_taint(alpha)


# ... -> source sanitizer -> transforms -> ...


def a_to_sanitize_a_to_x_to_b_no_issue():
    alpha = source_a()
    beta = sanitize_source_a_tito(alpha)
    gamma = transform_x(beta)
    sink_b(gamma)


def sanitize_a_transform_x_tito(arg):
    alpha = sanitize_source_a_tito(arg)
    return transform_x(alpha)


def a_to_sanitize_a_x_to_b_no_issue():
    alpha = source_a()
    beta = sanitize_a_transform_x_tito(alpha)
    sink_b(beta)


def sanitize_a_transform_x_sink_b_no_taint(arg):
    alpha = sanitize_source_a_tito(arg)
    beta = transform_x(alpha)
    sink_b(beta)


def sanitize_a_to_y_to_z_to_b_taint(arg):
    alpha = sanitize_source_a_tito(arg)
    beta = transform_y(alpha)
    gamma = transform_z(beta)
    sink_b(gamma)


def a_to_sanitize_a_yzb_no_issue(arg):
    alpha = source_a()
    sanitize_a_to_y_to_z_to_b_taint(alpha)


def axy_to_sanitize_a_yzb_issue(arg):
    alpha = taint_with_transform_yx()
    sanitize_a_to_y_to_z_to_b_taint(alpha)


# ... -> sink sanitizer -> ... (no transforms)


def c_to_sanitize_d_to_d_no_issue():
    alpha = source_c()
    beta = sanitize_sink_d_tito(alpha)
    sink_d(beta)


# ... -> transforms -> sink sanitizer -> ...


def a_to_x_to_sanitize_b_to_b_no_issue():
    alpha = source_a()
    beta = transform_x(alpha)
    gamma = sanitize_sink_b_tito(beta)
    sink_b(gamma)


def transform_x_sanitize_b_tito(arg):
    alpha = transform_x(arg)
    return sanitize_sink_b_tito(alpha)


def a_to_x_sanitize_b_to_b_no_issue():
    alpha = source_a()
    beta = transform_x_sanitize_b_tito(alpha)
    sink_b(beta)


def source_a_transform_x_sanitize_b_taint():
    alpha = source_a()
    beta = transform_x(alpha)
    return sanitize_sink_b_tito(beta)


def a_x_sanitize_b_to_b_no_issue():
    alpha = source_a_transform_x_sanitize_b_taint()
    sink_b(alpha)


def source_a_transform_y_transform_z_sanitize_b_no_taint():
    alpha = source_a()
    beta = transform_y(alpha)
    gamma = transform_z(beta)
    return sanitize_sink_b_tito(gamma)


# ... -> sink sanitizer -> transforms -> ...


def a_to_sanitize_b_to_x_to_b_issue():
    alpha = source_a()
    beta = sanitize_sink_b_tito(alpha)
    gamma = transform_x(beta)
    sink_b(gamma)


def sanitize_b_transform_x_tito(arg):
    alpha = sanitize_sink_b_tito(arg)
    return transform_x(alpha)


def a_to_sanitize_b_x_to_b_issue():
    alpha = source_a()
    beta = sanitize_b_transform_x_tito(alpha)
    sink_b(beta)


def source_a_sanitize_b_taint():
    alpha = source_a()
    return sanitize_sink_b_tito(alpha)


def a_sanitize_b_to_x_to_b_issue():
    alpha = source_a_sanitize_b_taint()
    beta = transform_x(alpha)
    sink_b(beta)


def a_sanitize_b_to_xb_issue():
    alpha = source_a_sanitize_b_taint()
    sink_taint_with_transform_x(alpha)


def source_a_sanitize_b_transform_x_taint():
    alpha = source_a()
    beta = sanitize_sink_b_tito(alpha)
    return transform_x(beta)


def a_sanitize_b_x_to_b_issue():
    alpha = source_a_sanitize_b_transform_x_taint()
    sink_b(alpha)


# ... -> transforms -> tito sanitizer -> ...


def transform_x_tito_sanitize_b(x, y):
    return transform_x(x)


def no_issue_transform_x_tito_sanitize_b():
    alpha = source_a()
    beta = transform_x_tito_sanitize_b(alpha)
    sink_b(beta)


def transform_x_tito_sanitize_b_all_parameters(x, y):
    return transform_x(x)


def no_issue_transform_x_tito_sanitize_b_all_parameters():
    alpha = source_a()
    beta = transform_x_tito_sanitize_b_all_parameters(alpha)
    sink_b(beta)


def transform_x_tito_global_sanitize_b(x, y):
    return transform_x(x)


def no_issue_transform_x_tito_global_sanitize_b():
    alpha = source_a()
    beta = transform_x_tito_global_sanitize_b(alpha)
    sink_b(beta)


def transform_x_tito_sanitize_return(x, y):
    return transform_x(x)


def no_issue_transform_x_tito_sanitize_return():
    alpha = source_a()
    beta = transform_x_tito_sanitize_return(alpha)
    sink_b(beta)


# additional sanitize propagation with transform tests


def tito_propagation_source_sanitizer_1(arg):
    alpha = sanitize_a_transform_x_tito(arg)
    return sanitize_source_c_tito(alpha)


def tito_propagation_source_sanitizer_2(arg):
    alpha = sanitize_source_c_tito(arg)
    return sanitize_a_transform_x_tito(alpha)


def tito_propagation_source_sanitizer_3(arg):
    alpha = transform_x_sanitize_a_tito(arg)
    return sanitize_source_c_tito(alpha)


def tito_propagation_source_sanitizer_4(arg):
    alpha = sanitize_source_c_tito(arg)
    return transform_x_sanitize_a_tito(alpha)


def tito_propagation_sink_sanitizer_1(arg):
    alpha = sanitize_b_transform_x_tito(arg)
    return sanitize_sink_d_tito(alpha)


def tito_propagation_sink_sanitizer_2(arg):
    alpha = sanitize_sink_d_tito(arg)
    return sanitize_b_transform_x_tito(alpha)


def tito_propagation_sink_sanitizer_3(arg):
    alpha = transform_x_sanitize_b_tito(arg)
    return sanitize_sink_d_tito(alpha)


def tito_propagation_sink_sanitizer_4(arg):
    alpha = sanitize_sink_d_tito(arg)
    return transform_x_sanitize_b_tito(alpha)


def transform_y_sanitize_b_tito(arg):
    alpha = transform_y(arg)
    return sanitize_sink_b_tito(alpha)


def tito_propagation_source_sink_sanitizers_mixed_1(arg):
    alpha = sanitize_a_transform_x_tito(arg)
    beta = sanitize_source_c_tito(alpha)
    gamma = sanitize_sink_d_tito(beta)
    return transform_y_sanitize_b_tito(gamma)


def tito_propagation_source_sink_sanitizers_mixed_2(arg):
    alpha = sanitize_source_c_tito(arg)
    beta = transform_y_sanitize_b_tito(alpha)
    gamma = sanitize_a_transform_x_tito(beta)
    return sanitize_sink_d_tito(gamma)


def sanitize_all(arg):
    ...


def transform_x_sanitize_all(arg):
    arg = sanitize_all(arg)
    arg = transform_x(arg)
    return arg

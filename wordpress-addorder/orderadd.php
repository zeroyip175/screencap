<?php
/**
 * Plugin Name: 批量創建訂單 for Woocommerce
 * Description: An tool that helps you create orders.
 * Version: 2.0.0
 * Author: MGT Eddie
 */

require_once 'random.php';

add_action('admin_menu', 'register_my_custom_menu_page');
function register_my_custom_menu_page()
{
    add_menu_page('批量創建訂單', '批量創建訂單', 'manage_options', 'oa', 'oa_page', '', 7);
}

function oa_get_product_id()
{
    $args = array(
        'post_type' => 'product',
        'posts_per_page' => - 1
    );
    $products = get_posts($args);
    return $products[array_rand($products) ]->ID;
}

function oa_page()
{
    echo '<link href="https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/css/bootstrap4-toggle.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/js/bootstrap4-toggle.min.js"></script>';
    echo '<div class="wrap"><h1 class="wp-heading-inline">批量創建訂單</h1></div>';
    echo '<hr class="wp-header-end">';
    echo '<form method="POST"><table class="form-table" role="presentation">';
    echo '<tbody>';
    echo '<tr><th class="row">訂單數量</th><td><input type="number" name="order_num" id="order_num" value="1" required="required" class="regular-text"></td></tr>';
    echo '<tr><th class="row">開始日期</th><td><input type="date" name="start_date" id="start_date" required="required" value="2023-01-01"></td></tr>';
    echo '<tr><th class="row">完結日期</th><td><input type="date" name="end_date" id="end_date" required="required" value="' . date('Y-m-d') . '"></td></tr>';
    echo '<tr><th class="row">地址</th><td><input type="checkbox" name="address_cb" class="form-check-input" checked></td></tr>';
    echo '<tr><th class="row">電話</th><td><input type="checkbox" name="telephone_cb" class="form-check-input" checked></td></tr>';
    echo '<tr><th class="row">Email</th><td><input type="checkbox" name="email_cb" class="form-check-input" checked></td></tr>';
    echo '</tbody>';
    echo '</table>';
    echo '<p class="submit">';
    echo '<input type="submit" name="submit" id="submit" class="button button-primary" value="創建訂單">';
    echo '</p></form>';
}

add_action('init', 'process_form');
function process_form()
{
    if (isset($_POST['submit']))
    {
        $plugin_path = trailingslashit(WP_PLUGIN_DIR) . 'woocommerce/woocommerce.php';
        if (
            in_array( $plugin_path, wp_get_active_and_valid_plugins() )
            || in_array( $plugin_path, wp_get_active_network_plugins() )
        ) {
            extract($_POST);
            for($i = 0; $i < $order_num; $i++){
                $isEng = rand(0,1);
                $gender = rand(0,1);
                $firstname = firstname($gender);
                $lastname = lastname();
                $email = email($firstname[1], $lastname[1]);
                $phone = '';
                $address_full = '';
                if(isset($address_cb)){
                    $address_full = address();
                }else {
                    $address_full = '';
                }
                if(isset($telephone_cb)){
                    $phone = phone();
                }else{
                    $phone = '';
                }
                if(!isset($email_cb)){
                    $email = '';
                }

                $address = array(
                    'first_name' => $firstname[$isEng?1:0],
                    'last_name' => $lastname[$isEng?1:0],
                    'email' => $email,
                    'phone' => $phone,
                    'address_1' => $address_full,
                    'address_2' => '',
                    'city' => 'Hong Kong',
                    'country' => 'HK'
                );

                $customer_data = array(
                    'first_name' => $firstname[$isEng?1:0],
                    'last_name'  => $lastname[$isEng?1:0],
                    'role'       => 'customer',
                );
                $user_name = explode("@", $email)[0];
                $customerID = wc_create_new_customer($email, $user_name, $user_name, $customer_data);

                $order_args = array(
                    'customer_id'   => $customerID,
                );

                $order = wc_create_order($order_args);
            
                // Set the payment date same as creation date
                $creation_date = rand(strtotime($start_date), strtotime($end_date));
                echo $creation_date;
                $order->set_date_created($creation_date);
                $order->set_date_paid($creation_date);

            
                $order->add_product(get_product(oa_get_product_id()), rand(1,3));
                $order->set_address($address, 'billing', '', true);
                $order->set_address($address, 'shipping', '', true);
                $order->calculate_totals();
                $order->update_status(order_status($i));
            }
            echo '<div class="notice notice-success">';
            echo '<p>已經創建 ' . $order_num. ' 個訂單</p>';
            echo '</div>';
        } else {
            echo '<div class="notice notice-error">';
            echo '<p>尚未安裝/啟用WooCommerce插件</p>';
            echo '</div>';
        }
    }
}


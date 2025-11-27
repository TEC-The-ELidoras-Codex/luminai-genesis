<?php
/*
Plugin Name: WP GitHub Webhook Receiver
Description: Receive GitHub webhooks and verify HMAC signature. Logs deliveries to wp-content/github-webhook.log
Version: 0.1
Author: The Elidoras Codex
*/

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

add_action('rest_api_init', function () {
    register_rest_route('myplugin/v1', '/github', [
        'methods' => 'POST',
        'callback' => 'myplugin_github_webhook',
        'permission_callback' => '__return_true',
    ]);
});

function myplugin_github_webhook(\WP_REST_Request $request) {
    $payload = $request->get_body();
    $secret = defined('GITHUB_WEBHOOK_SECRET') ? GITHUB_WEBHOOK_SECRET : getenv('GITHUB_WEBHOOK_SECRET');
    $signature = $request->get_header('x-hub-signature-256');

    if (!$signature || !$secret) {
        return new WP_REST_Response(['error' => 'missing signature or secret'], 400);
    }

    list($algo, $hash) = explode('=', $signature, 2) + array('', '');
    if ($algo !== 'sha256') {
        return new WP_REST_Response(['error' => 'unexpected signature algorithm'], 400);
    }

    $computed = hash_hmac('sha256', $payload, $secret);
    if (!hash_equals($computed, $hash)) {
        return new WP_REST_Response(['error' => 'invalid signature'], 401);
    }

    $data = json_decode($payload, true);
    if (!$data) {
        return new WP_REST_Response(['error' => 'invalid json'], 400);
    }

    $event = isset($_SERVER['HTTP_X_GITHUB_EVENT']) ? $_SERVER['HTTP_X_GITHUB_EVENT'] : '';
    $log = sprintf("[%s] event=%s repo=%s\n", date('c'), $event, $data['repository']['full_name'] ?? 'unknown');
    $logfile = WP_CONTENT_DIR . '/github-webhook.log';
    @file_put_contents($logfile, $log, FILE_APPEND);

    // TODO: add custom processing for push / pull_request events here

    return new WP_REST_Response(['ok' => true], 200);
}

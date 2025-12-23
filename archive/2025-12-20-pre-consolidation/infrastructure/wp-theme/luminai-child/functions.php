<?php
/**
 * Minimal child theme functions for LuminAI
*/

add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style( 'luminai-child-style', get_stylesheet_uri() );
} );

/**
 * Register a simple Publications sidebar
 */
add_action('widgets_init', function () {
  register_sidebar( array(
    'name'          => 'Publications Sidebar',
    'id'            => 'sidebar-publications',
    'description'   => 'Add publication cards here',
    'before_widget' => '<div class="publication-card">',
    'after_widget'  => '</div>',
  ) );
});

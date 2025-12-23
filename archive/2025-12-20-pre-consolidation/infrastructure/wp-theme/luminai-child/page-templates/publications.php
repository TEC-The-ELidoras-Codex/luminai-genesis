<?php
/*
Template Name: Publications
Description: A simple page template that lists 'publications' posts created for TGCR and other works.
*/
get_header();
?>

<main id="main" role="main">
  <div class="site-content">
    <h1>Publications</h1>
    <?php
    $args = array(
      'post_type' => 'post',
      'orderby' => 'date',
      'order' => 'DESC',
      'posts_per_page' => 20
    );
    $pubs = new WP_Query($args);
    if ($pubs->have_posts()) :
      while ($pubs->have_posts()) : $pubs->the_post();
        ?>
        <article class="publication-card">
          <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
          <p><?php the_excerpt(); ?></p>
        </article>
        <?php
      endwhile;
      wp_reset_postdata();
    else :
      echo '<p>No publications yet.</p>';
    endif;
    ?>
  </div>
</main>

<?php
get_footer();
?>

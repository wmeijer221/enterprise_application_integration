<script>
	import Header from './Header.svelte';
	import '../app.css';
</script>

<!-- Gradient background -->
<div>
	<Header />

	<main>
		<slot />
	</main>

	<footer>
		<p>
			<!-- <a href="https://example.com">Sentiment Analysis</a> -->
		</p>
	</footer>
</div>

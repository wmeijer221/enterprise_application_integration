<script lang="ts">
	import SearchBar from './SearchBar.svelte';

	let results: string[];
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<SearchBar {results} />
</section>

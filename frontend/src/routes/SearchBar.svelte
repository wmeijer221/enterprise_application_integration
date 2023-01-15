<script lang="ts">
	import { enhance } from '$app/forms';
	import { onMount } from 'svelte';
	import TitleCard from './TitleCard.svelte';

	export let results: string[];

	let searchTerm = '';
	let debouncedSearchTerm = '';

	async function search() {
		debouncedSearchTerm = searchTerm;
		const response = await fetch(
			`http://localhost:8000/titles/search?query=${debouncedSearchTerm}`
		);

		if (response.ok) {
			results = await response.json();
		}
	}

	onMount(async () => {
		search();
	});
</script>

<div class="p-4 px-28">
	<!-- prevent default -->
	<form method="POST" use:enhance>
		<label
			for="default-search"
			class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label
		>
		<div class="relative">
			<div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
				<svg
					aria-hidden="true"
					class="w-5 h-5 text-gray-500 dark:text-gray-400"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
					/></svg
				>
			</div>
			<input
				type="search"
				id="default-search"
				class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-zinc-500 focus:border-zinc-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-zinc-500 dark:focus:border-zinc-500"
				placeholder="Search Movies, Series, Actors..."
				required
				bind:value={searchTerm}
				on:input={search}
			/>
			<button
				type="submit"
				class="text-white absolute right-2.5 bottom-2.5 bg-zinc-700 hover:bg-zinc-800 focus:ring-4 focus:outline-none focus:ring-zinc-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-zinc-600 dark:hover:bg-zinc-700 dark:focus:ring-zinc-800"
				>Search</button
			>
		</div>
	</form>
	<div
		class="w-full text-md text-gray-50 border-2 border-gray-300 rounded-lg p-2 mt-8 bg-neutral-800"
	>
		{#if results}
			{#each results as result, i}
				<TitleCard {result} isLastElement={i == results.length - 1} />
			{/each}
		{/if}
	</div>
</div>

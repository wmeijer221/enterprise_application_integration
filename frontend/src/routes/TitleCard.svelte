<script lang="ts">
	export let result: any;
	export let isLastElement: boolean;
</script>

<!-- Title card result svelte component -->
<!-- Example object -->

<a href="/titles?id={result.uuid}">
	<div
		class="w-full p-4 pl-11 text-md border-solid border-gray-500 hover:bg-neutral-700 {isLastElement
			? ''
			: 'border-b'}"
	>
		<h2>{result.name}</h2>
	</div>
</a>

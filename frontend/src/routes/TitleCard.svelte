<script lang="ts">
	export let result: any;
	export let isLastElement: boolean;
	export let type: 'title' | 'actor';

	let url: string;

	$: {
		if (type === 'title') {
			url = `/titles?id=${result.uuid}`;
		} else if (type === 'actor') {
			url = `/actors?id=${result.uuid}`;
		}
	}
</script>

<!-- Title card result svelte component -->
<!-- Example object -->

<a href={url}>
	<div
		class="w-full p-4 pl-11 text-md border-solid border-gray-500 hover:bg-neutral-700 bg-neutral-800 {isLastElement
			? ''
			: 'border-b'}"
	>
		<h2>{result.name}</h2>
	</div>
</a>

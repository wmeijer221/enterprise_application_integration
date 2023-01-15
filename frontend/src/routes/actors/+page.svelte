<!-- Svelte Title Page -->
<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	const id = $page.url.searchParams.get('id');

	onMount(async () => {
		const ws = new WebSocket('ws://localhost:8082/titles/sentiment?actor_id=' + id);

		ws.onmessage = (event) => {
			console.log(event.data);
		};

		ws.onclose = (event) => {
			console.log('Socket is closed. Reconnect will be attempted in 1 second.', event.reason);

			console.log('Reason: ' + event.reason);
		};
	});
</script>

<div class="title-page">
	<h1>My Title</h1>
</div>

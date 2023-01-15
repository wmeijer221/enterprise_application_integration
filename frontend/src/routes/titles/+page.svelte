<!-- Svelte Title Page -->
<script lang="ts">
	import { page } from '$app/stores';
	import type { AverageSentiment, Review } from 'src/types';
	import { onMount } from 'svelte';
	import LineChart from '../LineChart.svelte';
	import PieChart from '../PieChart.svelte';
	import ReviewCard from '../ReviewCard.svelte';

	let ws: WebSocket;

	const id = $page.url.searchParams.get('id');
	let titleDetails: any = {};
	let averageSentiment: AverageSentiment = {
		avg_negativity: 0,
		avg_polarity: 0,
		avg_positivity: 0,
		count: 0
	};

	$: sentimentMessages = {} as Record<string, Review>;
	let negativeSentimentCount = 0;
	let positiveSentimentCount = 0;

	onMount(async () => {
		const titleDetailResponse = await fetch(`http://localhost:8000/title?id=${id}`);

		if (titleDetailResponse.ok) {
			titleDetails = await titleDetailResponse.json();
		}

		const titleSentimentResponse = await fetch(
			`http://localhost:8000/titles/sentiment?title_id=${id}`
		);

		if (titleSentimentResponse.ok) {
			averageSentiment = await titleSentimentResponse.json();
		}

		const sentimentMessagesResponse = await fetch(
			`http://localhost:8000/titles/sentiment/examples?title_id=${id}`
		);

		if (sentimentMessagesResponse.ok) {
			const newSentimentMessages = await sentimentMessagesResponse.json();

			newSentimentMessages.forEach((message: Review) => {
				sentimentMessages[message.uuid] = message;
			});
		}

		ws = new WebSocket('ws://localhost:8082/titles/sentiment?title_id=' + id);

		ws.onmessage = (event) => {
			const messageObject = JSON.parse(event.data);

			if (messageObject.type === 'connected') {
				console.log('Connected to websocket 🚀');
			} else if (messageObject.type === 'review') {
				const review = messageObject.body;
				sentimentMessages[review.uuid] = review;
			}
		};

		ws.onclose = (event) => {
			console.log('Socket is closed. Reconnect will be attempted in 1 second.', event.reason);

			console.log('Reason: ' + event.reason);
		};
	});

	// // TODO: Close the websocket when we navigate away from this page
	// onDestroy(() => {
	// 	if (ws) {
	// 		ws.close();
	// 	}
	// });

	// Update sentimentCount when sentimentMessages changes
	$: sentimentCount = Object.keys(sentimentMessages).length;

	// Update positiveSentimentCount and negativeSentimentCount when sentimentMessages changes
	$: {
		positiveSentimentCount = 0;
		negativeSentimentCount = 0;

		Object.values(sentimentMessages).forEach((message) => {
			if (message.sentiment.polarity >= 0) {
				positiveSentimentCount++;
			} else {
				negativeSentimentCount++;
			}
		});
	}
</script>

<div class="p-16 bg-gradient-to-b from-neutral-200 to-neutral-300 text-neutral-900">
	<h1 class="pb-2">{titleDetails.name}</h1>
	<!-- <div>
		{sentimentCount}
		{sentimentCount === 1 ? 'review' : 'reviews'}
	</div> -->

	<div class="grid grid-cols-4 gap-16">
		<div class="col-span-3 flex justify-center rounded-xl bg-neutral-900 p-2 md:p-10">
			<LineChart {sentimentMessages} />
		</div>

		<div class="flex justify-center rounded-xl bg-neutral-900 p-2 md:p-10">
			<PieChart {positiveSentimentCount} {negativeSentimentCount} />
		</div>
	</div>
	<div class="mt-8">
		<h3>
			{sentimentCount}
			{sentimentCount === 1 ? ' review' : ' reviews'}
		</h3>
		<div class="mt-2">
			{#each Object.values(sentimentMessages).sort((a, b) => new Date(b.timestamp).valueOf() - new Date(a.timestamp).valueOf()) as message}
				<ReviewCard {message} />
			{/each}
		</div>
	</div>
</div>

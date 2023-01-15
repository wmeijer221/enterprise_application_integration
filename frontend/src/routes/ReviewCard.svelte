<script lang="ts">
	import type { Review } from 'src/types';

	export let message: Review;

	let sentimentScore = message.sentiment.positivity + message.sentiment.negativity;

	console.log(message);

	let sourceLogo = '';

	if (message.source_name === 'reddit') {
		sourceLogo = '/reddit.png';
	} else if (message.source_name === 'twitter') {
		sourceLogo = '/twitter.png';
	} else if (message.source_name === 'imdb') {
		sourceLogo = '/imdb.png';
	}
</script>

<div class="w-full rounded-xl bg-neutral-900 p-8 pr-4 text-neutral-300 mb-8">
	<!-- Div with message.author and message.source_name -->
	<div class="flex justify-between border-b border-neutral-700 mb-2">
		<div class="flex mb-2">
			<img src={sourceLogo} class="w-6 mr-2" alt={message.source_name} />
			<span>{message.reviewer}</span>
		</div>
		<div>
			{message.timestamp}
		</div>
	</div>

	<div class="grid grid-cols-9 ">
		<div class="p-4 flex flex-col justify-center">
			<div class="flex justify-evenly text-3xl">
				<div class="p-5 rounded-lg {sentimentScore >= 0 ? 'bg-green-700' : 'bg-red-700'}">
					{sentimentScore > 0 ? '+' : ''}{sentimentScore}
				</div>
			</div>
		</div>
		<div class="col-span-8">
			{message.text.slice(0, 1000)}
			{message.text.length > 1000 ? '...' : ''}
		</div>
	</div>
</div>

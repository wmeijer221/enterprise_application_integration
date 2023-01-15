<script lang="ts">
	export let message: any;

	let sentimentScore = message.sentiment.positivity + message.sentiment.negativity;
</script>

<div class="grid grid-cols-6 w-full rounded-xl bg-neutral-900 py-8 pr-4 text-neutral-300 my-8">
	<div class="p-4 flex flex-col justify-center">
		<div class="flex justify-evenly text-3xl">
			<div class={sentimentScore >= 0 ? 'text-green-700' : 'text-red-700'}>
				{sentimentScore > 0 ? '+' : ''}{sentimentScore}
			</div>
		</div>
	</div>
	<div class="col-span-5">
		{message.text}
	</div>
</div>

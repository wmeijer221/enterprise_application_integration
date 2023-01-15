<!-- Svelte pie chart using tailwind -->
<script lang="ts">
	// import pie chart from chart.js
	import { Line } from 'svelte-chartjs';
	import 'chartjs-adapter-moment';

	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale,
		TimeScale
	} from 'chart.js';
	import type { Review } from 'src/types';

	export let sentimentMessages: Record<string, Review> = {};
	let timeseries: { x: Date; y: number }[] = [];

	ChartJS.register(
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale,
		TimeScale
	);

	$: {
		timeseries = Object.values(sentimentMessages)
			.map((message) => {
				return {
					x: new Date(message.timestamp),
					y: message.sentiment.polarity
				};
			})
			.sort((a, b) => a.x.valueOf() - b.x.valueOf());

		let totalPolarity = 0;

		for (let i = 0; i < timeseries.length; i++) {
			totalPolarity += timeseries[i].y;
			timeseries[i].y = totalPolarity;
		}
	}

	$: data = {
		datasets: [
			{
				label: 'Sentiment',
				data: timeseries,
				backgroundColor: ['rgba(0, 255, 0, 0.5)', 'rgba(255, 0, 0, 0.5)'],
				borderColor: ['rgba(0, 255, 0, 0.5)', 'rgba(255, 0, 0, 0.5)']
			}
		]
	};

	const options = {
		responsive: true,
		aspectRatio: 4,
		plugins: {
			title: {
				display: true,
				text: 'Sentiment over time'
			}
		},
		scales: {
			x: {
				type: 'time',
				time: {
					unit: 'day'
				}
			}
		}
	};

	$: console.log(timeseries.map((point) => point.y));
</script>

<Line {data} {options} />

<script>
    import * as req from '$lib/utils/request.js';
    // import { browser } from '$app/environment';
    import { onMount } from 'svelte';

    let decks;
    let cards;
    let images;
    async function getDecks() {
        await req.makeRequest('/decks/', 'GET')
            .then(rsp => { decks = rsp.decks; });
    }

    async function getFirstDeckCards() {
        await req.makeRequest('/cards/1', 'GET')
            .then(rsp => {
                cards = rsp.cards;
                console.log(cards);
                getCardFrontImages()
            })
    }

    async function getCardFrontImages() {
        cards.forEach(async (card) => {
            let imageUrl = `/data/images/${card.card_id}_front.jpg`
            await req.makeRequest(`/images/image?imageUrl=${imageUrl}`)
                .then(rsp => {
                    console.log(rsp);
                })
        })
    }

    onMount(() => {
        getDecks()
        getFirstDeckCards()
    })
</script>


<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

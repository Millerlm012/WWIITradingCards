-- cards with missing images
SELECT
	c.id
	, card_id
	, card_name
	, c.url
	, front_image_url
	, back_image_url
	, deck_id
	, d.full_name
	, d.deck_name
	, d.deck_number
	, d.url
FROM cards c
LEFT JOIN decks d on d.id = c.deck_id
WHERE front_image_url IS NULL OR back_image_url IS NULL;
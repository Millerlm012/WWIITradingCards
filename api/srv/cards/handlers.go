package cards

import (
	"net/http"
	"wwii_cards/api/utils"

	"github.com/gin-gonic/gin"
)

func GetCards(c *gin.Context) {
	deckId := c.Param("deckId")

	var cards []utils.Card
	utils.DB.Where("deck_id = ?", deckId).Find(&cards)

	c.JSON(http.StatusOK, gin.H{"cards": cards})
}

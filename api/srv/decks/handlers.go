package decks

import (
	"net/http"
	"wwii_cards/api/utils"

	"github.com/gin-gonic/gin"
)

func GetAllDecks(c *gin.Context) {
	var decks []utils.Deck
	utils.DB.Find(&decks).Order("id ASC")

	c.JSON(http.StatusOK, gin.H{"decks": decks})
}

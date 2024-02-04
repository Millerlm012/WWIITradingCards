package utils

import (
	"time"

	"github.com/glebarez/sqlite"
	"golang.org/x/exp/slog"
	"gorm.io/gorm"
)

var DB *gorm.DB

type Deck struct {
	Id          int       `json:"id" gorm:"primaryKey;index;not nulll;unique"`
	FullName    string    `json:"full_name"`
	Publisher   string    `json:"publisher"`
	DeckName    string    `json:"deck_name"`
	DeckNumber  int       `json:"deck_number"`
	Url         string    `json:"url"`
	Created     time.Time `json:"created"`
	LastUpdated time.Time `json:"last_updated"`
}

type Card struct {
	Id            int       `json:"id" gorm:"primaryKey;index;not nulll;unique"`
	CardId        string    `json:"card_id"`
	CardName      string    `json:"card_name"`
	Url           string    `json:"url"`
	FrontImageUrl string    `json:"front_image_url"`
	BackImageUrl  string    `json:"back_image_url"`
	Created       time.Time `json:"created"`
	LastUpdated   time.Time `json:"last_updated"`
	DeckId        int       `json:"-"`
}

func ConnectDatabase() {
	database, err := gorm.Open(sqlite.Open("/data/trading.db"), &gorm.Config{})
	if err != nil {
		slog.Error("Failed to connect to database!")
		panic(err)
	}

	DB = database
}

import random

from fireplace import game


def random_agent(game: ".game.Game") -> ".game.Game":
    # it's actually a random agent right now, but it'll be greedy
    player = game.current_player

    while True:
        # we don't want hero power, so it's commented below
        # heropower = player.hero.power
        # if heropower.is_usable() and random.random() < 0.1:
        #     if heropower.requires_target():
        #         heropower.use(target=random.choice(heropower.targets))
        #     else:
        #         heropower.use()
        #     continue

        # iterate over our hand and play whatever is playable
        for card in player.hand:
            if card.is_playable() and random.random() < 0.5:  # choose random cards
                target = None
                if card.must_choose_one:  # there are some choosable special skills
                    card = random.choice(card.choose_cards)
                if card.requires_target():  #
                    target = random.choice(card.targets)
                print("Playing %r on %r" % (card, target))
                card.play(target=target)

                if player.choice:  # chyba wybiera jakąś kartę???
                    choice = random.choice(player.choice.cards)
                    print("Choosing card %r" % (choice))
                    player.choice.choose(choice)

                continue

        # Randomly attack with whatever can attack
        for character in player.characters:
            if character.can_attack():
                character.attack(random.choice(character.targets))

        break

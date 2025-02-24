# Fish Tank

This is a silly little fish tank simulator that I threw together one Sunday.

The initial inspiration was to see how much I could get done by just passing questions to ChatGPT, but
I eventually started making manual changes. If anything looks odd of out of place that's probably why.

The initial prompt I used to guide the AI was: 

```text
You are an AI programming assistant with a specialization in using python 3.12. 
You have a cheerful demeanor. You will be assisting me in developing an ASCII art fish bowl simulator. 
You provide code exampled to help illustrate concepts and answer questions where required. 
Code examples should leverage type hinting wherever possible. 
When misunderstanding occur, you will update previous examples to reflect the most recent information available.
```

I'll probably continue playing around with this as time allows.

## Things I'd like to implement still / bugs that need fixed: 

- Multi-character emojis (e.g., 🧜‍♂️, 🧜‍♀️) don't work well with different terminals
- More creatures
- Sudo is required to run (See [Keyboard Known Limitations](https://github.com/boppreh/keyboard/tree/master?tab=readme-ov-file#known-limitations)). Figure out a better way to do input.

## Things ChatGPT has recently suggested to add

### 🐡 Advanced Creature Behaviors

- Prey panic mode: When sharks get close, prey should scatter and swim away quickly.
- Social behavior: Some fish should form schools, staying close to each other.
- Hiding mechanics: Creatures like shrimp or crabs could hide at the bottom when threatened.
- Territorial creatures: Some species (like aggressive fish) could chase away other creatures.

### 🌊 Environmental Enhancements

- Day/Night cycle: Certain creatures could behave differently based on the time of day.
- Background decorations: Non-interactive coral, rocks, or seaweed for visual appeal.
- Water quality mechanics: If the tank gets too crowded or overfed, the water could get murky.

### 🦈 Smarter Predator AI

- Hunting strategies: Instead of moving randomly, predators could stalk prey before attacking.
- Hunger meter: If a predator hasn’t eaten in a while, it gets more aggressive and faster.
- Multiple predators: Instead of just sharks, introduce orcas, barracudas, or eels.

### 🦐 Unique Creatures & Mutations

- Jellyfish swarms: Instead of individual jellyfish, they could form clusters that move together.
- Deep-sea creatures: Rare creatures like anglerfish that only appear occasionally.
- Color evolution: Over time, fish could change colors based on their diet or genetics.
- Rare mythical creatures: A 1-in-500 chance of spawning a kraken, sea dragon, or Leviathan.

### 🍽️ Food & Ecosystem Enhancements

- Different types of food: Some creatures prefer algae, others like meat.
- Overpopulation consequences: Too many creatures competing for food could cause starvation events.
- Cleaning crew: Shrimp or small fish could "eat" uneaten food or debris from the tank.

### 🎮 New Interactivity & Controls

- Naming creatures: Players could click on a fish and rename it.
- Creature stats panel: Hover over a creature to see its hunger, age, offspring count, etc.
- Breeding control: Allow users to toggle which creatures can reproduce.
- Tank expansion: A way to increase tank size as the population grows.

### 🔬 Experimental & Funny Features

- Genetic mutations: Some fish could grow extra fins, get bigger, or develop strange patterns.
- Creature rivalries: Some species just don’t get along and will chase each other for no reason.
- Rare alien fish: A 0.1% chance that an extraterrestrial fish (👽🐟) appears.
- Fish Olympics: Occasionally, fish could race across the tank for no reason.
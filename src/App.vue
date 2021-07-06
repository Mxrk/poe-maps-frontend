<template>
  <div id="app">
    <v-tour name="myTour" :steps="steps"></v-tour>
    <div class="content">
      <section class="headline">
        <h1>Map Trade</h1>
        <div id="league_selection">
          <h3>League:</h3>
          <div class="select" id="v-step-0">
            <select v-model="league">
              <option v-for="(league, key) in leagues" :value="key" :key="key">
                {{ league }}
              </option>
            </select>
          </div>
        </div>
      </section>
      <section class="inputs">
        <TagInput
          :itemsSelected="have"
          text="I have ..."
          :searching="isSearching"
          :error="Input1Error"
          id="v-step-1"
          :tutorialOpen="tutorialOpen"
        >
        </TagInput>
        <TagInput
          :itemsSelected="want"
          text="I want ..."
          :searching="isSearching"
          :error="Input2Error"
          id="v-step-5"
          :tutorialOpen="tutorialOpen"
        >
        </TagInput>
      </section>
      <section class="bottomline">
        <div class="username-input">
          <h3>Character:</h3>
          <div class="input" id="v-step-6">
            <input
              type="text"
              placeholder="Enter your character name"
              v-model="username"
              v-bind:class="{ error: CharacterError.length > 0 }"
            />
            <!-- <span> {{CharacterError}} </span> -->
          </div>
        </div>

        <template v-if="isSearching">
          <button id="search-button-stop" @click="stopSearch">Stop</button>
        </template>
        <template v-else>
          <button id="search-button" @click="startSearch">Search</button>
        </template>
      </section>
      <Matcher :connections="connections" :searching="isSearching"> </Matcher>
    </div>
    <footer class="footer">
      <div class="footer-items">
        <a @click="TourStart" class="footer-item"> tutorial </a>
        <a class="footer-item" href="https://poe.watch"> poe.watch </a>
        <a class="footer-item" href="https://poe.watch/privacy"> privacy </a>
        <a class="footer-item" href="https://github.com/Mxrk/poe-maps-frontend"> github </a>
      </div>
    </footer>
  </div>
</template>

<script>
import TagInput from "./components/TagInput.vue";
import Matcher from "./components/Matcher.vue";

export default {
  name: "App",
  components: {
    TagInput,
    Matcher,
  },
  data() {
    return {
      leagues: {
        Ultimatum: "Ultimatum",
        HCUltimatum: "HC Ultimatum",
        Standard: "Standard",
        HCStandard: "HC Standard",
      },
      league: 'Ultimatum',
      username: "",
      isSearching: false,
      socket: null,
      want: [],
      have: [],
      connections: [],
      Input1Error: "",
      Input2Error: "",
      CharacterError: "",
      tutorialOpen: false,
      steps: [
        {
          target: "#v-step-0",
          content: "Select your league.",
        },
        {
          target: "#v-step-1",
          content: "Select the maps you have.",
          params: {
            enableScrolling: false,
          },
        },
        {
          target: "#v-step-2",
          content: "You can either input a search term or...",
          before: () => new Promise((resolve) => {
            this.tutorialOpen = true;
            resolve("foo");
          }),
        },
        {
          target: "#v-step-3",
          content: "filter with a given tier.",
        },
        {
          target: "#v-step-4",
          content: "Select the tier of the wanted map.",
          params: {
            enableScrolling: false,
          },
          before: () => new Promise((resolve) => {
            resolve("foo");
          }),
        },
        {
          target: "#v-step-5",
          content: "Select the maps you want.",
          before: () => new Promise((resolve) => {
            this.tutorialOpen = false;
            const obj = { name: "Arcade Map", tier: 1 };
            this.have.push(obj);
            resolve("foo");
          }),
          params: {
            enableScrolling: false,
            placement: "top",
          },
        },
        {
          target: "#v-step-6",
          content: "Enter your current ingame character name.",
          before: () => new Promise((resolve) => {
            const obj = { name: "Coves Map", tier: 1 };
            this.want.push(obj);
            resolve("foo");
          }),
        },
        {
          target: "#search-button",
          content: "Start searching! :)",
          before: () => new Promise((resolve) => {
            this.username = "Tutorial";
            resolve("foo");
          }),
        },
        {
          target: ".Matcher",
          content: "Now you can see your connections",
          before: () => new Promise((resolve) => {
            this.isSearching = true;
            const obj = [
              {
                want: [{ name: "Coves Map", tier: 1, region: "" }],
                have: [{ name: "Arcade Map", tier: 1, region: "" }],
                userid: "5577006791947779410",
                username: "A",
              },
            ];
            this.connections = obj;
            resolve("foo");
          }),
        },
        {
          target: "#button",
          content:
            "Whisper the player ingame, the message get's automatically copied into your clipboard.",
        },
        {
          target: ".match",
          content: "Done, have fun using the page!",
          params: {
            placement: "top",
          },
        },
        {
          target: ".content",
          content: " ",
          params: {
            placement: "top",
          },
          before: () => new Promise((resolve) => {
            // Time-consuming UI/async operation here
            window.location.reload();
            resolve("foo");
          }),
        },
      ],
    };
  },
  mounted() {
    this.initSocket();
  },
  methods: {
    startSearch() {
      if (this.want.length > 0 && this.have.length > 0 && this.username.length > 0) {
        this.sendMessage();
        this.isSearching = true;
      } else {
        if (this.want.length === 0) {
          this.Input1Error = "placeholder";
        }
        if (this.have.length === 0) {
          this.Input2Error = "placeholder";
        }
        if (this.username.length === 0) {
          this.CharacterError = "please enter your character name.";
        }
      }
    },
    stopSearch() {
      this.isSearching = false;
      this.sendDCMessage();
      this.connections = [];
    },
    initSocket() {
      this.socket = new WebSocket("wss://trade.poe.watch/ws");
      this.socket.onopen = () => {
        this.ready = true;
      };

      this.socket.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        // disconnect
        if (msg.status_code === 1) {
          // remove url from connections
          const filtered = this.connections.filter((value) => value.userid !== msg.user_id);
          this.connections = filtered.reverse();
          return;
        }

        const temp = this.connections.concat(msg).reverse();
        this.connections = temp;
      };

      this.socket.onclose = () => {
        this.socket.send("Client closed!");
      };

      this.socket.onerror = () => {
      };
    },
    sendMessage() {
      this.searching = true;
      const want = this.want.map((elem) => ({
        name: elem.name,
        tier: elem.tier,
      }));

      const have = this.have.map((elem) => ({
        name: elem.name,
        tier: elem.tier,
      }));
      const msg = {
        want,
        have,
        status_code: 0,
        username: this.username,
        league: this.league,
      };
      this.socket.send(JSON.stringify(msg));
    },
    sendDCMessage() {
      if (!this.ready) {
        return;
      }
      const msg = { status_code: 1 };
      this.socket.send(JSON.stringify(msg));
      this.searching = false;
    },
    TourStart() {
      this.$tours.myTour.start();
    },
  },
  watch: {
    have() {
      this.stopSearch();
    },
    want() {
      this.stopSearch();
    },
    username() {
      this.stopSearch();
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: whitesmoke;
  display: flex;
  flex-direction: column;
  height: 100%;
}

body,
html {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  background-color: #1a2133;
}

@media (max-width: 768px) {
  button {
    width: 100% !important;
  }
}

.headline {
  display: flex;
  width: 100%;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
}

#league_selection {
  display: flex;
  align-items: center;
  margin-right: 1em;
}

#league_selection select {
  margin-left: 0.5rem;
}

/* Reset Select */
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  appearance: none;
  outline: 0;
  box-shadow: none;
  border: 0 !important;
  background: #2c3e50;
  background-image: none;
}

/* Custom Select */
.select {
  position: relative;
  display: flex;
  margin-left: 1em;
  width: 10em;
  height: 3em;
  line-height: 3;
  background: #2c3e50;
  overflow: hidden;
  border-radius: 0.2em;
}

select {
  flex: 1;
  padding: 0 0.5em;
  color: #fff;
  cursor: pointer;
}

/* Arrow */
.select::after {
  content: "\25BC";
  position: absolute;
  top: 0;
  right: 0;
  padding: 0 1em;
  background: transparent;
  cursor: pointer;
  pointer-events: none;
  -webkit-transition: 0.25s all ease;
  -o-transition: 0.25s all ease;
  transition: 0.25s all ease;
}

.inputs {
  display: flex;
  margin-top: 1em;
  flex-wrap: wrap;
}

.bottomline {
  display: flex;
  margin-right: 1em;
  margin-top: 1em;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.username-input {
  display: flex;
  align-items: center;
}

.username-input h3 {
  margin-right: 1em;
}

.username-input input {
  height: 2em;
  background-color: #000000;
  border-color: transparent;
  color: whitesmoke;
  /* border: 1px solid #1C1B22;
  border-radius: 5px; */
}

.input {
  display: flex;
  flex-direction: column;
}

.input span {
  color: #af0606;
}

.error {
  border-color: #af0606 !important;
}

#search-button {
  width: 15em;
  height: 3em;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2c3a60;
  color: whitesmoke;
  border: none;
}

#search-button-stop {
  width: 15em;
  height: 3em;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ee6c4d;
  color: whitesmoke;
  border: none;
}

.content {
  flex: 1 0 auto;
  padding: 1em;
  margin: 2.5em auto;
}

footer {
  background: #42a5f5;
  color: white;
}

.footer {
  flex-shrink: 0;
  padding: 20px;
  background-color: #d9d7d7;
  color: black;
  text-align: center;
}

.footer a {
  margin: 1em;
  text-decoration: none;
  color: black;
}

a:visited {
  text-decoration: none;
}

.footer-item:hover {
  color: white;
  cursor: pointer;
}
</style>

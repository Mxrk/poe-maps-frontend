<template>
  <div class="Matcher">
    <h1 v-if="searching"> Connections </h1>
    <div v-if="searching && connections.length == 0" class="lds-ripple"><div></div><div></div></div>
    <div v-for="con in connections" :key="con.id" class="match">
      <div class="message">
        <span id="whisperText" v-bind:class="{ lined: con.messaged }">
          User {{ con.username }} wants {{ getMaps(con.want) }} and has
          {{ getMaps(con.have) }}</span
        >
      </div>

      <div class="buttons">
        <button id="button" @click="copyWhisper(con, index)">Whisper</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["connections", "searching"],
  data() {
    return {
      players: [],
    };
  },
  methods: {
    copyWhisper(connection, index) {
      const text = `@${
        connection.username
      } Hey, I would like to trade my ${this.getMaps(connection.want)} for your ${this.getMaps(connection.have)}!`;
      navigator.clipboard.writeText(text);
      connection.messaged = true;
      this.$set(this.connections, index, connection);
    },
    getMaps(mapArray) {
      const a = [];
      for (let i = 0; i < mapArray.length; i += 1) {
        const element = mapArray[i];
        a.push(`T${element.tier}:${element.name}`);
      }
      return a;
    },
  },
  watch: {
  },
};
</script>

<style scoped>

.Matcher{
  display: flex;
  align-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column;
}
.match {
  background-color: #000000;
  margin-top: 0.6em;
  display: flex;
  justify-content: space-between;
  align-content: center;
  align-items: center;
  height: 2.5em;
  width: 100%;
}

.buttons {
  margin-right: 1em;
}

.lined {
  text-decoration: line-through;
}

.message{
  margin-left: 1em;
}

.lds-ripple {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto;
}

.lds-ripple div {
  position: absolute;
  border: 4px solid #fff;
  opacity: 1;
  border-radius: 50%;
  animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}

.lds-ripple div:nth-child(2) {
  animation-delay: -0.5s;
}

@keyframes lds-ripple {
  0% {
    top: 36px;
    left: 36px;
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    top: 0px;
    left: 0px;
    width: 72px;
    height: 72px;
    opacity: 0;
  }
}

#button {
  width: 8em;
  height: 2em;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2c3a60;
  color: whitesmoke;
  border: transparent;
}

#button:active {
  background: #e5e5e5;
  -webkit-box-shadow: inset 0px 0px 5px #c1c1c1;
     -moz-box-shadow: inset 0px 0px 5px #c1c1c1;
          box-shadow: inset 0px 0px 5px #c1c1c1;
   outline: none;
}
</style>

<template>
  <div class="tag-input-whole">
    <label for="input">{{text}}</label>
    <div class="tag-input" v-bind:class="{error: error.length > 0 }">
      <div v-for="(tag, index) in itemsSelected" :key="tag.id" class="tag-input_tag">
        <div class="tier">T:{{ tag.tier }}</div>
        <div class="tag-content">
          {{ tag.name }}
        </div>
        <span @click="removeTag(index)">x</span>
      </div>
      <input
        type="text"
        placeholder="Enter a map"
        class="tag-input_text"
        @input="onChange"
        @click="onChange"
        v-model="search"
        name="input"
        id="v-step-2"
      />
    </div>
    <div class="search" v-show="isOpen">
      <ul class="map-list">
        <li v-for="map in results" :key="map.id" class="autocomplete-result">
          <div>
            <template v-if="tierFilter == 'All'">
            <img :src="map.icon + map.tiers[0]" id="mapIcon" loading="lazy">
            </template>
            <template v-else>
            <img :src="map.icon + tierFilter" id="mapIcon" loading="lazy">
            </template>
          </div>
          <div>
          {{ map.name}}
          </div>
          <section class="tier-selection" id="v-step-4">
             <a v-for="m in map.tiers" :key="m.id" class="tier-selection-item">
               <span v-bind:class="{ active: tierFilter === m}" @click="addMap(map, m)">
              T{{m}}
               </span>
            </a>
          </section>
        </li>
      </ul>
      <div class="filter-section" id="v-step-3">
        Tier filter:
        <a class="filter-section-tier" v-for="m in tiers" :key="m.id"
        @click="changeFilterTier(m)"
        v-bind:class="{ active: tierFilter === m || tierFilter === 'All' && m === 'All'}">
        {{m}}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import maps from "../assets/maps_tier_sorted.json";

export default {
  name: "TagInput",
  props: ["itemsSelected", "text", "searching", "error", "tutorialOpen"],
  data() {
    return {
      search: "",
      results: [],
      items: maps.maps,
      isOpen: false,
      tiers: ['All', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
      tierFilter: 'All',
    };
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  destroyed() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    addMap(map, tier) {
      const obj = { name: map.name, tier };

      // check if map is already selected
      for (let i = 0; i < this.itemsSelected.length; i += 1) {
        const element = this.itemsSelected[i];
        if (element.name === obj.name && element.tier === obj.tier) {
          return;
        }
      }

      this.itemsSelected.push(obj);
      this.search = "";
      this.filterResults();
    },
    removeTag(index) {
      this.itemsSelected.splice(index, 1);
    },
    filterResults() {
      this.results = this.items.filter((item) => item.name.toLowerCase().indexOf(this.search.toLowerCase()) > -1);
    },
    onChange() {
      this.isOpen = true;

      if (this.search === "") {
        this.results = this.items;
        return;
      }
      this.filterResults();
    },
    setResult(result) {
      this.itemsSelected.push(result);
      this.search = "";
      this.isOpen = false;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target) && !this.tutorialOpen) {
        this.isOpen = false;
      }
    },
    changeFilterTier(tier) {
      if (tier === 'All') {
        this.results = this.items;
        this.tierFilter = tier;
        return;
      }
      this.results = this.items.filter((item) => item.tiers.includes(tier));
      this.tierFilter = tier;
    },
  },
  watch: {
    tutorialOpen(val) {
      if (val === true && this.text === "I have ...") {
        this.onChange();
      }
    },
  },
};
</script>

<style scoped>
.tag-input-whole {
  margin-right: 1em;
}

.tag-input {
  font-size: 0.9em;
  box-sizing: border-box;
  padding: 0 1em;
  display: flex;
  background-color: #000000;
  flex-wrap: wrap;
  min-width: 35vw;
  max-width: 35vw;
  align-items: center;
}

.search {
  background-color: #000000;
  border: none;
  min-height: 15em;
  max-height: 15em;
  min-width: 35vw;
  max-width: 35vw;
  overflow: hidden;
}

@media (max-width: 768px) {
  .tag-input{
  min-width: 90vw;
  max-width: 90vw;
  }

  .search{
  min-width: 90vw;
  max-width: 90vw;
  }
}

.map-list {
  max-height: 10em;
  min-height: 10em;
  overflow: auto;
  padding-left: 1em;
}

.tier {
  margin-right: 0.5em;
}

.tag-content {
  margin-right: 0.5em;
  padding: 0;
}

.tag-input_tag {
  height: 2em;
  float: left;
  margin-right: 0.5em;
  background-color: #4f5973;
  line-height: 1rem;
  padding: 0 1em;
  border-radius: 1em;
  display: flex;
  align-items: center;
  margin-top: 0.2em;
}

.tag-input_tag > span {
  cursor: pointer;
  opacity: 0.75;
}

.tag-input_text {
  border: none;
  outline: none;
  font-size: 0.9em;
  line-height: 50px;
  background: none;
  color: whitesmoke;
}

.autocomplete-results {
  padding: 0;
  margin: 0;
  border: 1px solid #eeeeee;
  height: 120px;
  min-height: 1em;
  max-height: 6em;
  overflow: auto;
  display: flex;
}

.autocomplete-result:hover{
  color: #8E9EC3;
  cursor: pointer;
}

.autocomplete-result {
  display: flex;
  list-style: none;
  text-align: left;
  padding: 4px 2px;
  cursor: pointer;
  align-items: center;
}

.filter-section {
  margin-left: 1em;
}

.filter-section-tier{
  color:#303849
}

.filter-section-tier:hover{
  color: #8E9EC3;
  cursor: pointer;
}

.tier-selection{
  margin-left: 0.5em;
  color:#303849
}

.active{
  color: #8E9EC3;
}

.tier-selection-item:hover{
  color:#8E9EC3;
  cursor: pointer;
}

#mapIcon{
  height: 28px;
  width: 28px;
  margin-right: 0.5em;
}

.error{
  border-color: #AF0606 !important;
  border-bottom: 2px solid #AF0606;
}
</style>

<template>
  <div v-if="showInitContent">
    <init-content @search="deliver"></init-content>
  </div>
  <div v-else>
    <after-content ref="realSearch"></after-content>
  </div>
</template>

<script>
import InitContent from './InitContent.vue'
import AfterContent from './AfterContent.vue'

export default {
  data() {
    return {
      showInitContent: true,
    }
  },
  components: {
    AfterContent,
  },
  methods: {
    deliver(question) {
      this.showInitContent = false;
      this.$nextTick(() => {
        this.$refs.realSearch.search(question);
      })
    },
  }
}
</script>

<style scoped>
</style>
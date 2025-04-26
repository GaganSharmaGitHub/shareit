<script lang="ts">
  import { sharedStateStore, type SharedState } from "./lib/store/appState";
  $: sharedState = $sharedStateStore as SharedState;
</script>

<main>
  <h1>Share it</h1>
</main>

<style>
</style>

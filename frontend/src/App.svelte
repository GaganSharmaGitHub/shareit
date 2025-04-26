<script lang="ts">
  import { sharedStateStore, type SharedState } from "./lib/store/appState";
  import Login from "./lib/components/Login.svelte";
  import { userApi } from "./lib/store/utils/api/user";

  $: sharedState = $sharedStateStore as SharedState;

  let userName: string | null = null;

  async function checkLogin() {
    try {
      const response = await userApi.getMe();
      if (response.success) {
        const { name } = response.data;
        userName = name;
      } else {
        userName = "Not logged in";
        localStorage.removeItem("authToken");
      }
    } catch (error) {
      userName = "Not logged in";
      localStorage.removeItem("authToken");
    }
  }

  function handleLogin(username: string, password: string) {
    const authToken = btoa(`${username}:${password}`);
    localStorage.setItem("authToken", authToken);
    userName = username;
    checkLogin();
  }

  checkLogin();

  $: showLogin = userName === "Not logged in";
</script>

<main>
  <h1>Share it</h1>
  {#if showLogin}
    <Login onLogin={handleLogin} />
  {/if}
  {#if userName !== "Not logged in"}
    <p>Welcome, {userName}!</p>
  {/if}
</main>

<style>
  p {
    margin-top: 10px;
    color: red;
  }
</style>

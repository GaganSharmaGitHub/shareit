<script lang="ts">
  let usernameInput: string = "";
  let passwordInput: string = "";
  let loginMessage: string | null = null;

  export let onLogin: (username: string, password: string) => void;

  function handleLogin() {
    if (usernameInput && passwordInput) {
      onLogin(usernameInput, passwordInput);
      loginMessage = "Login successful! Token saved in localStorage.";
    } else {
      loginMessage = "Please provide both username and password.";
    }
  }
</script>

<div>
  <h2>Login</h2>
  <input type="text" placeholder="Username" bind:value={usernameInput} />
  <input type="password" placeholder="Password" bind:value={passwordInput} />
  <button on:click={handleLogin}>Login</button>
  {#if loginMessage}
    <p>{loginMessage}</p>
  {/if}
</div>

<style>
  div {
    margin-top: 20px;
  }

  input {
    display: block;
    margin-bottom: 10px;
    padding: 8px;
    font-size: 14px;
  }

  button {
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
  }

  p {
    margin-top: 10px;
    color: red;
  }
</style>

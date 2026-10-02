document.addEventListener("submit", async (event) => {
  const form = event.target;

  if (
    !(form instanceof HTMLFormElement) ||
    !form.matches(".bubble-actions form")
  ) {
    return;
  }

  event.preventDefault();

  const button = form.querySelector(".upvote-button");
  const count = button.querySelector("span:last-child");
  button.disabled = true;

  try {
    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        Accept: "application/json",
      },
      credentials: "same-origin",
    });

    if (response.redirected) {
      window.location.assign(response.url);
      return;
    }

    if (!response.ok) {
      throw new Error("Vote request failed");
    }

    const result = await response.json();
    count.textContent = result.upvotes;
  } catch {
    const status = form.querySelector(".vote-status");
    if (status) {
      status.textContent = "Could not record your vote. Please try again.";
    }
  } finally {
    button.disabled = false;
  }
});

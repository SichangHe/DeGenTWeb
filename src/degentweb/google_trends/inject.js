;(function () {
  let topicsHeader, queriesHeader, selectedTopAll

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
  }

  function findTopicsAndQueries() {
    if (queriesHeader != undefined) return

    const topicsOrQueriesTitles = Array.from(
      document.querySelectorAll("div.fe-atoms-generic-title"),
    )
    const topicsTitle = topicsOrQueriesTitles.find((node) =>
      node.innerText.includes("topics"),
    )
    if (topicsTitle == undefined) throw new Error("topicsTitle is undefined")
    topicsHeader = topicsTitle.parentNode
    topicsHeader.scrollIntoView()

    const queriesTitle = topicsOrQueriesTitles.find((node) =>
      node.innerText.includes("queries"),
    )
    if (queriesTitle == undefined) throw new Error("queriesTitle is undefined")
    queriesHeader = queriesTitle.parentNode
  }

  async function selectTopAll() {
    if (selectedTopAll) return
    findTopicsAndQueries()
    const style = document.createElement("style")
    style.textContent = "* { transition: none !important; };"
    document.head.appendChild(style)
    for (const header of [topicsHeader, queriesHeader]) {
      const orderButton = header.querySelector("md-select")
      if (orderButton == undefined) throw new Error("orderButton is undefined")
      orderButton.click()
      await sleep(100)
      const orderTop = Array.from(
        document.querySelectorAll("md-option:not(.ng-hide)"),
      ).find((node) => node.checkVisibility() && node.innerText.includes("Top"))
      if (orderTop == undefined) throw new Error("orderTop is undefined")
      orderTop.click()
      await sleep(100)
    }
    selectedTopAll = true
  }

  function getAllEntriesOf(blockHeader) {
    const body = blockHeader.nextElementSibling.children[0]
    const items = body.querySelectorAll("div.item")
    const nextButton = body.querySelectorAll("button.md-button")[1]
    console.assert(nextButton != undefined, "nextButton is undefined")
    const entries = []
    while (true) {
      for (const item of items) {
        if (!item.checkVisibility()) continue
        const href = item.querySelector("a.progress-label").href
        const text = item
          .querySelector("div.progress-label-wrapper")
          .title.replace(/^Explore /, "")
        const [name, maybeClass] = text.split(" - ")
        const classification = maybeClass || null
        const valStr = item.querySelector("div.progress-value").innerText.trim()
        const interest = parseInt(valStr)
        entries.push({ name, interest, href, classification })
      }
      if (nextButton.disabled) break
      nextButton.click()
    }
    return entries
  }

  async function getTopicsAndQueries() {
    try {
      await selectTopAll()
      const topics = getAllEntriesOf(topicsHeader)
      const queries = getAllEntriesOf(queriesHeader)
      return { topics, queries }
    } catch (err) {
      return { err: err.message }
    }
  }

  return getTopicsAndQueries()
})() // NOTE: No semicolon here for the value!

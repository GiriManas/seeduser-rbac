const handleDownload = async () => {
  if (!results) return;

  try {
    const sessionId = results.id;

    const response = await fetch(`/api/download-results?sessionId=${sessionId}`, {
      method: "GET",
      headers: {
        "x-access-token": yourAccessTokenHere  // Replace with real token or fetch from auth context
      }
    });

    if (!response.ok) {
      throw new Error("Failed to download the file.");
    }

    const blob = await response.blob();

    // Try to extract filename from response header
    let filename = "results.xlsx";
    const disposition = response.headers.get("Content-Disposition");
    if (disposition) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match?.[1]) {
        filename = match[1];
      }
    }

    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

  } catch (error) {
    console.error("Error downloading Excel:", error);
    alert("Download failed. Check console for details.");
  }
};
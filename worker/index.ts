const json = (body: unknown, status = 200) =>
  Response.json(body, {
    status,
    headers: {
      "cache-control": "no-store",
    },
  });

const worker = {
  fetch(request: Request): Response {
    const url = new URL(request.url);

    if (url.pathname === "/api/health") {
      return json({
        ok: true,
        service: "vijay-kumaran-portfolio-world",
        stage: "app-foundation",
      });
    }

    if (url.pathname.startsWith("/api/")) {
      return json(
        {
          ok: false,
          error: "not_found",
        },
        404,
      );
    }

    return new Response(null, { status: 404 });
  },
};

export default worker;

const ORIGENES_PERMITIDOS = new Set([
  "https://elitejerseys-es.netlify.app",
  "https://elitejerseys.pages.dev",
  "http://localhost:4321",
]);

export default {
  async fetch(request, env) {
    const origen = request.headers.get("Origin");

    if (!ORIGENES_PERMITIDOS.has(origen)) {
      return new Response("Origen no permitido", {
        status: 403,
      });
    }

    const headers = {
      "Access-Control-Allow-Origin": origen,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "Vary": "Origin",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers,
      });
    }

    const url = new URL(request.url);

    if (
      request.method !== "POST" ||
      url.pathname !== "/siguiente"
    ) {
      return new Response(
        JSON.stringify({
          error: "Solicitud no permitida",
        }),
        { status: 405, headers }
      );
    }

    try {
      // Protección contra solicitudes abusivas
      const ip =
        request.headers.get("CF-Connecting-IP") || "unknown";

      const { success } = await env.LIMITADOR.limit({
        key: ip,
      });

      if (!success) {
        return new Response(
          JSON.stringify({
            error: "Demasiadas solicitudes. Inténtalo en un minuto.",
          }),
          { status: 429, headers }
        );
      }

      // Incrementar el contador global sin duplicados
      const resultado = await env.DB.prepare(`
        UPDATE contador
        SET ultimo_numero = ultimo_numero + 1
        WHERE id = 1
        RETURNING ultimo_numero
      `).first();

      if (!resultado) {
        throw new Error("Contador no disponible");
      }

      const numero = resultado.ultimo_numero;

      // Generar la referencia del presupuesto
      return new Response(
        JSON.stringify({
          numero,
          referencia: `PRES-${String(numero).padStart(4, "0")}`,
        }),
        { status: 200, headers }
      );

    } catch (error) {
      console.error(error);

      return new Response(
        JSON.stringify({
          error: "No se pudo generar el presupuesto",
        }),
        { status: 500, headers }
      );
    }
  },
};
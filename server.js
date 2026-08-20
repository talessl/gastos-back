import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import sqlite3 from "sqlite3";
import { open } from "sqlite";

const db = await open({
  filename: "./banco-dados.sqlite", // Ele vai criar este arquivo na sua pasta!
  driver: sqlite3.Database,
});

await db.exec(`
  CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL,
    tipo TEXT,
    observacao TEXT,
    data TEXT
  )
`);

// 1. O Cardápio (TypeDefs)
// Define o formato da transação e quais perguntas (Query) ou ações (Mutation) podemos fazer
const typeDefs = `#graphql
  type Transacao {
    valor: Float
    tipo: String
    observacao: String
    data: String
  }

  type Query {
    buscarTransacoes: [Transacao]
  }

  type Mutation {
    adicionarTransacao(valor: Float, tipo: String, observacao: String, data: String): Transacao
    limparTransacoes: Boolean
  }
`;

// 3. Os Cozinheiros (Resolvers)
// Eles executam exatamente o que foi definido no cardápio (TypeDefs)
const resolvers = {
  Query: {
    buscarTransacoes: async () => {
      return await db.all("SELECT * FROM transacoes");
    },
  },
  Mutation: {
    // O "_" é porque não usamos o primeiro parâmetro, e o "args" contém os dados que o Front-end mandou
    adicionarTransacao: async (_, args) => {
      const resultado = await db.run(
        "INSERT INTO transacoes (valor, tipo, observacao, data) VALUES (?, ?, ?, ?)",
        [args.valor, args.tipo, args.observacao, args.data],
      );

      return { id: resultado.lastID, ...args };
    },
    limparTransacoes: async () => {
      await db.run("DELETE FROM transacoes");
      return true;
    },
  },
};

// 4. Subindo o servidor GraphQL
const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
});

console.log(`🚀 Servidor GraphQL conectado ao SQLite e rodando em ${url}`);

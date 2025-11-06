using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;

namespace dblab1.Data
{
    public class DbContext : IDisposable
    {
        private readonly SqlConnection _connection;
        private SqlTransaction _transaction;

        public DbContext(string connectionString)
        {
            _connection = new SqlConnection(connectionString);
            _connection.Open();
        }

        public SqlCommand CreateCommand(string commandText, bool isStoredProcedure = true)
        {
            var cmd = _connection.CreateCommand();
            cmd.CommandText = commandText;
            cmd.Transaction = _transaction;
            if (isStoredProcedure)
                cmd.CommandType = CommandType.StoredProcedure;
            return cmd;
        }

        public void BeginTransaction() => _transaction = _connection.BeginTransaction();
        public void Commit() => _transaction?.Commit();
        public void Rollback() => _transaction?.Rollback();

        public void Dispose()
        {
            _transaction?.Dispose();
            _connection?.Close();
        }
    }
}

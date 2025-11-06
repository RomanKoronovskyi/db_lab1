using dblab1.Data.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dblab1.Data
{
    public class UnitOfWork : IDisposable
    {
        private readonly DbContext _context;

        public ProjectRepository Projects { get; }
        public TaskRepository Tasks { get; }

        public UnitOfWork(string connectionString)
        {
            _context = new DbContext(connectionString);
            Projects = new ProjectRepository(_context);
            Tasks = new TaskRepository(_context);
        }

        public void Commit() => _context.Commit();
        public void Dispose() => _context.Dispose();
    }
}

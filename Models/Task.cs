using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dblab1.Models
{
    public class Task
    {
        public int ID { get; set; }
        public int ProjectId { get; set; }
        public int AssignedToUserId { get; set; }
        public int StatusId { get; set; }
        public int PriorityId { get; set; }
        public bool IsDeleted { get; set; }
        public int? UpdatedByUserId { get; set; }
    }
}

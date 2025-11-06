using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace dblab1.Models
{
    public class Project
    {
        public int ID { get; set; }
        public string ProjectName { get; set; }
        public int ClientId { get; set; }
        public int ManagerId { get; set; }
        public int StatusId { get; set; }
        public int? TeamId { get; set; }
        public int? UpdatedByUserId { get; set; }
    }
    public class ProjectDetails
    {
        public int ID { get; set; }
        public string ProjectName { get; set; }
        public string ClientName { get; set; }
        public string ManagerName { get; set; }
        public string StatusName { get; set; }
        public string TeamName { get; set; }
    }
}

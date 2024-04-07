
 const NavBar = () => {
    return (
        <div>

                <nav class="navbar navbar-expand-lg fixed-top"  >
                    <div class="container">
                        <a class="navbar-brand  me-auto" href="#!">shem Interiors</a>
                        <button  class="navbar-toggler" type="button" data-mdb-toggle="collapse" 
                        data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                        aria-label="Toggle navigation">
                        <i class="fas fa-bars"></i>
                        </button>
        
                            <div  class="collapse navbar-collapse ms-5 " id="navbarSupportedContent">
                            
                                <ul class="navbar-nav me-auto">
                                        <li   class="nav-item" >
                                            <a class="nav-link" href="#!">Home</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link" href="#!">About</a>
                                        </li>
                                        <li   class="nav-item" >
                                            <a class="nav-link" href="#!">Home</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link" href="#!">About</a>
                                        </li>
                                        <li   class="nav-item" >
                                            <a class="nav-link" href="#!">Home</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link" href="#!">About</a>
                                        </li>
                                </ul> 

                            
                                <ul class="navbar-nav d-flex flex-row">
                                        <li class="nav-item me-3 me-lg-0">
                                            <a class="nav-link" href="#!">
                                            <i class="fas fa-phone-alt link-success"></i>
                                            </a>
                                        </li>

                                        <li class="nav-item me-3 me-lg-0">
                                            <a class="nav-link" href="#!">
                                            <i class="fab fa-facebook-f link-primary"></i>
                                            </a>
                                        </li>
                                        <li class="nav-item me-3 me-lg-0">

                                            <a class="nav-link" href="#!">
                                            <i class="fab fa-whatsapp link-success"></i>
                                            </a>
                                        </li>
                                        <li class="nav-item me-3 me-lg-0">
                                            <a class="nav-link" href="#!">
                                            <i class="fab fa-twitter link-primary"></i>
                                            </a>
                                        </li>
                                        <li class="nav-item me-3 me-lg-0">
                                            <a class="nav-link" href="#!">
                                            <i class="fab fa-instagram link-danger"></i>
                                            </a>
                                        </li>
                                </ul> 

                            
                            </div>

                           
                    </div>
                </nav>
            
        </div>
        
    )
} 


export default NavBar;
